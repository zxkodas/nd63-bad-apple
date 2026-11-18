"""Stored per-key animation on the IROK ND63 (LED mode 25, the vendor app's "GIF").

The stock firmware ignores live per-key frames, but it keeps an uploaded animation in flash and
plays it by itself. Format from the vendor web app's CommonKBRY5088 class (setUserGifStart /
setUserGif), which the ND63 (ry5088_jc_gk8145g_1m_8k) uses:

    start:  12 00 00 00 00 00 00 ck                      then wait 300 ms
    frame:  12 <frame> <page 0..6> 01 <count> <delay lo> <delay hi> ck + 56 RGB bytes, 5 ms apart
    ck = 255 - (sum(bytes 0..6) & 255)

The frame count is one byte, so at most 255 frames. One upload is one flash write, so don't loop
uploads.

    python gif.py test                 4 frames: number row, Q row, A row, Z row (250 ms each)
    python gif.py badapple [--frames 255] [--start 0] [--length 0] [--threshold 0.5]
    python gif.py play                 start mode 25 and the music together
    python gif.py restore              back to your saved LED mode
"""
import argparse
import json
import subprocess
import sys
import time

import numpy as np

from nd63 import SAVED, Board, complement

PER_KEY_GIF = 25
SLOTS = 126
VIDEO = "media/bad_apple.mkv"

# Slot -> key, from the vendor's default matrix for ry5088_jc_gk8145g_1m_8k (index = slot).
MATRIX_KEYS = [
    None, "Esc", "Tab", "Caps", "LShift", "LCtrl", None, "1", "Q", "A", None, "LMeta",
    None, "2", "W", "S", "Z", "LAlt", None, "3", "E", "D", "X", None, None, "4", "R", "F", "C",
    None, None, "5", "T", "G", "V", None, None, "6", "Y", "H", "B", "Space", None, "7", "U", "J",
    "N", None, None, "8", "I", "K", "M", None, None, "9", "O", "L", ",", "RAlt", None, "0", "P",
    ";", ".", None, None, "-", "[", "'", "/", "Left", None, "=", "]", None, "RShift", "Down",
    None, "Backspace", "\\", "Enter", "Up", "Right", None, None, None, None, "Delete",
]

# Physical layout, 15 units wide, 5 rows: (key, x, width) per row.
ROWS = [
    [("Esc", 0, 1)] + [(k, 1 + i, 1) for i, k in enumerate("1234567890-=")] + [("Backspace", 13, 2)],
    [("Tab", 0, 1.5)] + [(k, 1.5 + i, 1) for i, k in enumerate("QWERTYUIOP[]")] + [("\\", 13.5, 1.5)],
    [("Caps", 0, 1.75)] + [(k, 1.75 + i, 1) for i, k in enumerate("ASDFGHJKL;'")] + [("Enter", 12.75, 2.25)],
    [("LShift", 0, 2.25)] + [(k, 2.25 + i, 1) for i, k in enumerate("ZXCVBNM,./")]
    + [("RShift", 12.25, 0.75), ("Up", 13, 1), ("Delete", 14, 1)],
    [("LCtrl", 0, 1.25), ("LMeta", 1.25, 1.25), ("LAlt", 2.5, 1.25), ("Space", 3.75, 7.25),
     ("RAlt", 11, 1), ("Left", 12, 1), ("Down", 13, 1), ("Right", 14, 1)],
]
WIDTH, HEIGHT = 15, 5


def key_rects():
    """slot -> (x0, y0, x1, y1) in key units."""
    where = {k: (x, y, x + w, y + 1) for y, row in enumerate(ROWS) for k, x, w in row}
    rects = {}
    for s, k in enumerate(MATRIX_KEYS):
        if k is not None:
            rects[s] = where[k]
    assert len(rects) == 63, len(rects)
    return rects


def gif_header(frame, page, count, delay_ms):
    head = [0x12, frame, page, 1, count, delay_ms & 255, (delay_ms >> 8) & 255]
    head.append(complement(head))
    return head


def upload(board, frames, delay_ms):
    """frames: list of 126-long lists of (r, g, b). One flash write for the whole animation."""
    count = len(frames)
    if not 1 <= count <= 255:
        sys.exit(f"{count} frames: the format holds 1..255")
    start = [0x12, 0, 0, 0, 0, 0, 0]
    start.append(complement(start))
    board.set_feature(bytes(start))
    time.sleep(0.3)
    t0 = time.monotonic()
    for i, colors in enumerate(frames):
        data = bytearray(7 * 56)
        for s, (r, g, b) in enumerate(colors[:SLOTS]):
            data[s * 3:s * 3 + 3] = bytes((r, g, b))
        for page in range(7):
            board.set_feature(bytes(gif_header(i, page, count, delay_ms)) + bytes(data[page * 56:(page + 1) * 56]))
            time.sleep(0.008)
        print(f"\ruploaded {i + 1}/{count}", end="", flush=True)
    print(f"  ({time.monotonic() - t0:.1f} s)")


def show(board):
    with open(SAVED) as f:
        saved = json.load(f)
    board.set_led(PER_KEY_GIF, *saved[1:])


def lit(slots, color=(255, 255, 255)):
    out = [(0, 0, 0)] * SLOTS
    for s in slots:
        out[s] = color
    return out


def test_frames():
    rects = key_rects()
    return [lit([s for s, r in rects.items() if r[1] == row]) for row in range(4)]


def badapple_frames(n, start, length, threshold, invert, crop=1.0):
    """crop: share of the video's height kept (centred). 1.0 squashes the whole 4:3 frame into
    the 3:1 board; 0.444 keeps true proportions (cuts top and bottom)."""
    fps = n / length
    px = 10  # pixels per key unit
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(length), "-i", VIDEO, "-an",
         "-vf", f"fps={fps},crop=iw:ih*{crop},scale={WIDTH * px}:{HEIGHT * px}",
         "-pix_fmt", "gray", "-f", "rawvideo", "-"],
        check=True, capture_output=True,
    ).stdout
    video = np.frombuffer(raw, np.uint8).reshape(-1, HEIGHT * px, WIDTH * px)[:n] / 255.0
    rects = key_rects()
    frames = []
    for img in video:
        on = []
        for s, (x0, y0, x1, y1) in rects.items():
            v = img[int(y0 * px):int(y1 * px), int(x0 * px):int(x1 * px)].mean()
            if (v < threshold) if invert is True else (v >= threshold):
                on.append(s)
        if invert == "auto" and len(on) > len(rects) // 2:
            # Light the smaller part (usually the figure), whichever colour it is.
            on = [s for s in rects if s not in on]
        frames.append(lit(on))
    return frames


def preview(frames, every):
    rects = key_rects()
    for i in range(0, len(frames), every):
        grid = [[" "] * (WIDTH * 2) for _ in range(HEIGHT)]
        for s, (x0, y0, x1, _) in rects.items():
            ch = "#" if frames[i][s][0] else "."
            for x in range(int(x0 * 2), int(x1 * 2)):
                grid[int(y0)][x] = ch
        print(f"frame {i}\n" + "\n".join("".join(r) for r in grid))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["test", "badapple", "play", "restore", "preview"])
    ap.add_argument("--frames", type=int, default=255)
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--length", type=float, default=0, help="seconds of video, 0 = to the end")
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument("--invert", action="store_true")
    ap.add_argument("--delay", type=int, default=250, help="ms per frame, test only")
    a = ap.parse_args()

    if a.cmd in ("badapple", "preview"):
        total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                      "-of", "csv=p=0", VIDEO], capture_output=True, text=True).stdout)
        length = a.length or total - a.start
        frames = badapple_frames(a.frames, a.start, length, a.threshold, a.invert)
        delay = round(length * 1000 / len(frames))
        print(f"{len(frames)} frames, {delay} ms each, {length:.1f} s of video")
        if a.cmd == "preview":
            return preview(frames, max(1, len(frames) // 8))

    board = Board()
    try:
        if a.cmd == "test":
            upload(board, test_frames(), a.delay)
            show(board)
        elif a.cmd == "badapple":
            upload(board, frames, delay)
            show(board)
        elif a.cmd == "play":
            show(board)
            subprocess.run(["ffplay", "-v", "error", "-nodisp", "-vn", "-autoexit", VIDEO],
                           stdin=subprocess.DEVNULL, check=False)
        elif a.cmd == "restore":
            with open(SAVED) as f:
                board.set_led(*json.load(f))
    finally:
        board.close()


if __name__ == "__main__":
    main()
