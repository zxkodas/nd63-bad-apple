"""Bad Apple!! on the IROK ND63 as whole-board brightness, in sync with the music.

The ND63's stock firmware ignores live per-key frames (0x0F), but follows the whole-board
screen-sync colour (0x0E, LED mode 21). So each video frame becomes one colour: the frame's
mean brightness. The LED mode you had before is restored on exit, whatever happens.

    python play.py                       full run
    python play.py --start 30 --length 10
    python play.py --color 255,40,80 --gamma 1.6 --invert
"""
import argparse
import json
import os
import signal
import subprocess
import sys
import time

import numpy as np

from nd63 import SAVED, Board

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(HERE, "media", "bad_apple.mkv")
TRACK = os.path.join(HERE, "media", "brightness.npy")
FPS = 30
W, H = 32, 24
SCREEN_SYNC = 21


def brightness_track():
    """Mean luminance per frame, 0..1, cached next to the video."""
    if os.path.exists(TRACK) and os.path.getmtime(TRACK) > os.path.getmtime(VIDEO):
        return np.load(TRACK)
    print("decoding video once...", flush=True)
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", VIDEO, "-an", "-vf", f"fps={FPS},scale={W}:{H}",
         "-pix_fmt", "gray", "-f", "rawvideo", "-"],
        check=True, capture_output=True,
    ).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H * W)
    track = frames.mean(axis=1) / 255.0
    np.save(TRACK, track)
    return track


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=float, default=0, help="seconds into the video")
    ap.add_argument("--length", type=float, default=0, help="seconds to play, 0 = to the end")
    ap.add_argument("--color", default="255,255,255", help="R,G,B for full white")
    ap.add_argument("--gamma", type=float, default=1.0, help=">1 darkens the greys")
    ap.add_argument("--invert", action="store_true")
    ap.add_argument("--offset", type=float, default=0.12, help="audio start latency to wait out, s")
    ap.add_argument("--mute", action="store_true")
    a = ap.parse_args()

    track = brightness_track()
    if a.invert:
        track = 1.0 - track
    track = track ** a.gamma
    tint = np.array([int(c) for c in a.color.split(",")], dtype=float)
    first = int(a.start * FPS)
    last = len(track) if a.length <= 0 else min(len(track), first + int(a.length * FPS))

    with open(SAVED) as f:
        saved = json.load(f)
    board = Board()
    audio = None
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        board.set_led(SCREEN_SYNC, *saved[1:])
        board.screen_color(0, 0, 0)
        if not a.mute:
            audio = subprocess.Popen(
                ["ffplay", "-v", "error", "-nodisp", "-vn", "-autoexit", "-ss", str(a.start),
                 *(["-t", str(a.length)] if a.length > 0 else []), VIDEO],
                stdin=subprocess.DEVNULL,
            )
            time.sleep(a.offset)
        t0 = time.monotonic()
        while True:
            i = first + int((time.monotonic() - t0) * FPS)
            if i >= last:
                break
            # Sent every frame, changed or not: screen sync may fall back if left unfed.
            board.screen_color(*(int(v) for v in np.clip(tint * track[i], 0, 255)))
            next_at = t0 + (i - first + 1) / FPS
            time.sleep(max(0.0, next_at - time.monotonic()))
    except KeyboardInterrupt:
        pass
    finally:
        if audio and audio.poll() is None:
            audio.terminate()
        board.screen_color(0, 0, 0)
        board.set_led(*saved)
        board.close()
        print("restored your lighting", flush=True)


if __name__ == "__main__":
    main()
