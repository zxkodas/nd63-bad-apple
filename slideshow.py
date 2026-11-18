"""Bad Apple!! on the IROK ND63 as a per-key slideshow through the stored User Picture.

The ND63's stock firmware has no live per-key path and no animation mode. What it does have is
the web app's custom image (LED mode 13, 5 slots), which writes flash on every upload. So this
re-uploads one slot again and again while mode 13 shows it. EVERY FRAME IS A FLASH WRITE: keep the
frame rate low and don't loop it. After a full run the keyboard can lag on typing; unplugging and
replugging it fixes that (seen 2026-11-18).

Upload format (vendor CommonKBRY5088 _setLightPic): 7 pages of
    0C <slot> FF <page> <len: 56, 42 on page 6> <last: 1 on page 6> 00 <ck> + 56 RGB bytes
126 slots x RGB = 378 bytes, slot order = the keyboard's matrix (gif.MATRIX_KEYS).
Mode 13 shows it: 07 0D <speed> <bright> <slot << 4> 00 C8 C8 <ck8>.

    python slideshow.py test                 4 uploads, 3 s apart, timed
    python slideshow.py clip --start 60 --length 10 --fps 1
    python slideshow.py run --fps 1          full song with music
"""
import argparse
import json
import subprocess
import time

from gif import VIDEO, badapple_frames, key_rects, lit
from nd63 import SAVED, Board, complement

USER_PICTURE = 13
SLOT = 0
PIC_BYTES = 378


def upload_picture(board, colors, slot=SLOT, page_gap=0.005):
    data = bytearray(7 * 56)
    for s, (r, g, b) in enumerate(colors[:126]):
        data[s * 3:s * 3 + 3] = bytes((r, g, b))
    for page in range(7):
        last = page == 6
        head = [0x0C, slot, 0xFF, page, PIC_BYTES - 56 * 6 if last else 56, 1 if last else 0, 0]
        head.append(complement(head))
        board.set_feature(bytes(head) + bytes(data[page * 56:(page + 1) * 56]))
        time.sleep(page_gap)


def show_picture(board, slot=SLOT):
    with open(SAVED) as f:
        _, speed, bright, *_ = json.load(f)
    cmd = [0x07, USER_PICTURE, speed, bright, slot << 4, 0, 200, 200]
    cmd.append(complement(cmd))
    board.set_feature(bytes(cmd))
    time.sleep(0.05)


def alive(board):
    try:
        return board.query(0x87)[1] == USER_PICTURE
    except OSError:
        return False


def restore(board):
    with open(SAVED) as f:
        board.set_led(*json.load(f))


def play(board, frames, fps, audio_start=None, audio_length=None, double=False, show_video=False):
    """Upload frames on a fixed clock. Stops at the first sign of trouble.

    double: write each frame into the slot that is NOT on screen (0/1 alternating), then switch
    the display to it, so the keys never show a half-written picture.
    """
    audio = None
    show_picture(board)
    if audio_start is not None:
        audio = subprocess.Popen(
            ["ffplay", "-v", "error", *([] if show_video else ["-nodisp", "-vn"]),
             "-window_title", "Bad Apple (keyboard follows this)", "-autoexit", "-ss", str(audio_start),
             *(["-t", str(audio_length)] if audio_length else []), VIDEO],
            stdin=subprocess.DEVNULL)
    t0 = time.monotonic()
    worst = 0.0
    try:
        skipped = unchanged = 0
        last_sent = None
        for i, colors in enumerate(frames):
            wait = t0 + i / fps - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            elif -wait > 1 / fps:
                skipped += 1  # behind the music: drop this frame (also one flash write saved)
                continue
            if colors == last_sent:
                unchanged += 1  # same keys lit as on screen: no upload, no flash, no flash write
                continue
            last_sent = colors
            started = time.monotonic()
            if double:
                slot = i % 2
                upload_picture(board, colors, slot)
                show_picture(board, slot)
            else:
                upload_picture(board, colors)
            took = time.monotonic() - started
            worst = max(worst, took)
            print(f"\rframe {i + 1}/{len(frames)}  upload {took * 1000:.0f} ms  worst {worst * 1000:.0f} ms"
                  f"  behind {skipped}  unchanged {unchanged}",
                  end="", flush=True)
        time.sleep(1 / fps)
    finally:
        print()
        if audio and audio.poll() is None:
            audio.terminate()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["test", "clip", "run", "restore"])
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--length", type=float, default=0)
    ap.add_argument("--fps", type=float, default=5, help="5 is smooth on the ND63; 10 struggles on all-white scenes")
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument("--invert", action="store_true", help="light the dark parts of the video")
    ap.add_argument("--auto", action="store_true", help="each frame, light whichever part is smaller")
    ap.add_argument("--video", action=argparse.BooleanOptionalAction, default=True,
                    help="show the video in a window while it plays (--no-video for music only)")
    ap.add_argument("--crop", type=float, default=1.0,
                    help="share of the video height kept: 1 = squash all, 0.444 = true proportions")
    ap.add_argument("--double", action="store_true", help="alternate slots 0/1; tested: MORE flashing (the mode switch flashes too)")
    a = ap.parse_args()

    board = Board()
    try:
        if a.cmd == "restore":
            return
        if a.cmd == "test":
            rects = key_rects()
            show_picture(board)
            for row in range(4):
                t = time.monotonic()
                upload_picture(board, lit([s for s, r in rects.items() if r[1] == row]))
                took = time.monotonic() - t
                print(f"upload {row + 1}: {took * 1000:.0f} ms, keyboard answers: {alive(board)}", flush=True)
                time.sleep(3)
            return
        total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                      "-of", "csv=p=0", VIDEO], capture_output=True, text=True).stdout)
        length = a.length or total - a.start
        n = max(1, round(length * a.fps))
        frames = badapple_frames(n, a.start, length, a.threshold, "auto" if a.auto else a.invert, a.crop)
        print(f"{len(frames)} frames = {len(frames)} flash writes, {a.fps} fps")
        play(board, frames, a.fps, a.start, a.length or None, a.double, a.video)
        print("keyboard answers:", alive(board))
    finally:
        try:
            restore(board)
            board.close()
        except OSError:
            # The keyboard reset itself (it drops off USB and comes back): reopen and restore.
            print("keyboard dropped off USB; waiting for it to come back...", flush=True)
            for _ in range(20):
                time.sleep(0.5)
                try:
                    board = Board()
                    break
                except (OSError, SystemExit):
                    continue
            restore(board)
            board.close()
        print("restored your lighting")


if __name__ == "__main__":
    main()
