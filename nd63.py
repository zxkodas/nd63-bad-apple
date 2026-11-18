"""IROK ND63 RGB (USB 3151:502d) live per-key lighting over the vendor HID interface.

Only these opcodes are ever sent: 0x0F (live colour frame, RAM only), 0x8F (identify),
0x87 (read LED mode) and 0x07 (set LED mode). Never 0x0C (writes flash), 0xAC (flash erase)
or anything else.

Frame layout (from canvas-rgb royuan.rs, checked on 3151:4015): 7 feature reports,
`0F 01 <page> 38 <last> 00 00 <ck>` then 56 RGB bytes, ck = 255 - (sum(bytes 0..6) & 255),
126 slots = 21 columns x 6 rows, column-major, bottom row first.

    python nd63.py selftest
    python nd63.py info                 identify + save the current LED mode to saved_led.json
    python nd63.py solid R G B [-s 5]   stream one colour
    python nd63.py cycle [-s 3]         red, green, blue, white
    python nd63.py mode 21              set LED mode (0x07), keeps the saved colour/speed/brightness
    python nd63.py restore              put back the LED mode in saved_led.json
    python nd63.py column N / row N     light one grid column (0..20) or row (0..5, 0 = bottom)
"""
import argparse
import fcntl
import glob
import json
import os
import sys
import time

VID, PID = 0x3151, 0x502D
SLOTS, COLS, ROWS = 126, 21, 6
PAGES, PAGE_DATA = 7, 56
REPORT = 64
HERE = os.path.dirname(os.path.abspath(__file__))
SAVED = os.path.join(HERE, "saved_led.json")

WHITE, BLACK = (255, 255, 255), (0, 0, 0)


def _ioc(direction, nr, size):
    return (direction << 30) | (size << 16) | (ord("H") << 8) | nr


HIDIOCSFEATURE = _ioc(3, 0x06, REPORT + 1)
HIDIOCGFEATURE = _ioc(3, 0x07, REPORT + 1)


def complement(values):
    return 255 - (sum(values) & 255)


# frame_reports and selftest are adapted from canvas-rgb tools/kbd-map.py
# (https://github.com/iAmChumby/canvas-rgb, Apache-2.0).
def frame_reports(colors):
    """The seven 64-byte payloads of one live frame (report id not included)."""
    payload = bytearray(PAGES * PAGE_DATA)
    for slot, (r, g, b) in enumerate(list(colors)[:SLOTS]):
        payload[slot * 3:slot * 3 + 3] = bytes((r, g, b))
    out = []
    for page in range(PAGES):
        head = [0x0F, 0x01, page, PAGE_DATA, 1 if page == PAGES - 1 else 0, 0, 0]
        head.append(complement(head))
        out.append(bytes(head) + bytes(payload[page * PAGE_DATA:(page + 1) * PAGE_DATA]))
    return out


def slot(col, row):
    """Grid cell to slot: column-major, row 0 = bottom."""
    return col * ROWS + row


def find_vendor_hidraw():
    want = f"HID_ID=0003:{VID:08X}:{PID:08X}"
    for node in sorted(glob.glob("/sys/class/hidraw/hidraw*")):
        try:
            with open(f"{node}/device/uevent") as f:
                if want not in f.read().upper():
                    continue
            with open(f"{node}/device/report_descriptor", "rb") as f:
                desc = f.read()
        except OSError:
            continue
        if desc[:3] == b"\x06\xff\xff":
            return "/dev/" + os.path.basename(node)
    return None


class Board:
    def __init__(self, path=None):
        self.path = path or find_vendor_hidraw()
        if not self.path:
            sys.exit("ND63 vendor interface (3151:502d, usage page 0xFFFF) not found")
        self.fd = os.open(self.path, os.O_RDWR)

    def close(self):
        os.close(self.fd)

    def set_feature(self, data):
        buf = bytearray(REPORT + 1)
        buf[1:1 + len(data)] = data
        fcntl.ioctl(self.fd, HIDIOCSFEATURE, buf)

    def get_feature(self):
        buf = bytearray(REPORT + 1)
        fcntl.ioctl(self.fd, HIDIOCGFEATURE, buf)
        return bytes(buf)

    def query(self, op):
        cmd = [op, 0, 0, 0, 0, 0, 0]
        cmd.append(complement(cmd))
        self.set_feature(bytes(cmd))
        time.sleep(0.02)
        reply = self.get_feature()
        # hidraw puts the report number first; accept the echo at [0] or [1].
        if reply[1] == op:
            return reply[1:]
        if reply[0] == op:
            return reply[:-1]
        raise RuntimeError(f"no echo for 0x{op:02X}: {reply[:16].hex(' ')}")

    def set_led(self, mode, speed, brightness, optflags, r, g, b):
        cmd = [0x07, mode, speed, brightness, optflags, r, g, b]
        cmd.append(complement(cmd))
        self.set_feature(bytes(cmd))
        time.sleep(0.05)

    def screen_color(self, r, g, b):
        """0x0E: one colour for the whole board, shown in mode 21 (Screen Sync)."""
        cmd = [0x0E, r, g, b, 0, 0, 0]
        cmd.append(complement(cmd))
        self.set_feature(bytes(cmd))

    def frame(self, colors):
        for report in frame_reports(colors):
            self.set_feature(report)

    def stream(self, colors_fn, seconds, fps=30):
        """colors_fn(t) -> 126 colours. Sends every 1/fps s for `seconds`."""
        t0 = time.monotonic()
        while (t := time.monotonic() - t0) < seconds:
            self.frame(colors_fn(t))
            time.sleep(max(0.0, 1 / fps - ((time.monotonic() - t0) - t)))


def solid(c):
    return [c] * SLOTS


def selftest():
    colors = [BLACK] * SLOTS
    colors[0], colors[9], colors[125] = (1, 2, 3), (255, 0, 0), (7, 8, 9)
    reps = frame_reports(colors)
    assert len(reps) == 7 and all(len(r) == 64 for r in reps)
    for page, r in enumerate(reps):
        last = 1 if page == 6 else 0
        assert r[:8] == bytes([0x0F, 0x01, page, 56, last, 0, 0, 0xB7 - page - last]), page
    assert reps[6][7] == 0xB0
    assert reps[0][8:11] == bytes([1, 2, 3])
    assert reps[0][8 + 27:8 + 30] == bytes([255, 0, 0])
    assert reps[6][8 + 39:8 + 42] == bytes([7, 8, 9])
    assert not any(reps[6][8 + 42:])
    print("selftest ok")


def led_tuple(reply):
    return list(reply[1:8])  # mode, speed, brightness, optflags, r, g, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("args", nargs="*", type=int)
    ap.add_argument("-s", "--seconds", type=float, default=5)
    ap.add_argument("--fps", type=float, default=30)
    a = ap.parse_args()

    if a.cmd == "selftest":
        return selftest()

    board = Board()
    try:
        if a.cmd == "info":
            print("hidraw:", board.path)
            ident = board.query(0x8F)
            print("identify:", ident[:16].hex(" "), "id =", int.from_bytes(ident[1:5], "little"))
            led = board.query(0x87)
            print("led 0x87:", led[:16].hex(" "))
            if not os.path.exists(SAVED):
                with open(SAVED, "w") as f:
                    json.dump(led_tuple(led), f)
                print("saved to", SAVED)
            else:
                print("kept existing", SAVED, open(SAVED).read())
        elif a.cmd == "solid":
            board.stream(lambda _t: solid(tuple(a.args[:3])), a.seconds, a.fps)
        elif a.cmd == "cycle":
            seq = [(255, 0, 0), (0, 255, 0), (0, 0, 255), WHITE]
            board.stream(lambda t: solid(seq[min(int(t / a.seconds), 3)]), a.seconds * 4, a.fps)
        elif a.cmd in ("column", "row"):
            n = a.args[0]
            cells = [slot(n, r) for r in range(ROWS)] if a.cmd == "column" else [slot(c, n) for c in range(COLS)]
            colors = [BLACK] * SLOTS
            for s in cells:
                colors[s] = WHITE
            board.stream(lambda _t: colors, a.seconds, a.fps)
        elif a.cmd == "probe2":
            # Halves swapping red/green each second: nothing stored on the board looks like that.
            def halves(t):
                left, right = ((255, 0, 0), (0, 255, 0)) if int(t) % 2 == 0 else ((0, 255, 0), (255, 0, 0))
                return [left if s // ROWS < COLS // 2 else right for s in range(SLOTS)]

            with open(SAVED) as f:
                saved = json.load(f)
            try:
                for mode in (13, 25):
                    print(f"phase: mode {mode} + 0x0F halves", flush=True)
                    board.set_led(mode, *saved[1:])
                    board.stream(halves, a.seconds, a.fps)
                print("phase: mode 21 + 0x0E whole-board cycle", flush=True)
                board.set_led(21, *saved[1:])
                seq = [(255, 0, 0), (0, 255, 0), (0, 0, 255), WHITE]
                t0 = time.monotonic()
                while (t := time.monotonic() - t0) < a.seconds:
                    board.screen_color(*seq[int(t) % 4])
                    time.sleep(1 / a.fps)
            finally:
                board.set_led(*saved)
                print("restored", flush=True)
        elif a.cmd == "mode":
            with open(SAVED) as f:
                saved = json.load(f)
            board.set_led(a.args[0], *saved[1:])
            print("led now:", board.query(0x87)[:9].hex(" "))
        elif a.cmd == "restore":
            with open(SAVED) as f:
                board.set_led(*json.load(f))
            print("led now:", board.query(0x87)[:9].hex(" "))
        else:
            sys.exit(f"unknown command {a.cmd}")
    finally:
        board.close()


if __name__ == "__main__":
    main()
