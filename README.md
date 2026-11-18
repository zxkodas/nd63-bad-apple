# nd63-bad-apple

Bad Apple!! on the per-key RGB of an **IROK ND63** keyboard, in sync with the music, on Linux.

The keyboard's stock firmware has no way to stream per-key colours live. What it does have is the
"custom image" feature from its web app (light mode 13). So this re-uploads that image over and over,
one video frame at a time, while the song plays. It works, with some catches (below).

## What you need

- An IROK ND63 (`3151:502d`) connected by USB cable, on Linux. Other boards: see
  [COMPATIBLE.md](COMPATIBLE.md).
- Python 3 with numpy, ffmpeg (includes ffplay), and yt-dlp to fetch the video.
- Read/write access to the keyboard's `/dev/hidraw*` node. Most desktops give the logged-in user
  this already; check with `python3 nd63.py info`.

No other Python packages: the scripts talk to hidraw directly with `ioctl`.

## Run it

```sh
mkdir -p media
yt-dlp -f 'bv*[height<=360]+ba/b[height<=360]/b' --merge-output-format mkv \
  -o 'media/bad_apple.%(ext)s' 'https://www.youtube.com/watch?v=FtutLA63Cp8'

python3 nd63.py info          # identifies the board and saves your current lighting
python3 slideshow.py run      # full song, 5 fps, video window + music
```

Your lighting is restored when it ends or on Ctrl+C. Useful options:

| option | effect |
|---|---|
| `--fps 3` | gentler on the keyboard (default 5; 10 struggles on all-white scenes) |
| `--crop 0.6` | taller shapes, cuts the top and bottom (default 1 = whole frame squashed) |
| `--auto` | light whichever part is smaller each frame (colours flip between scenes) |
| `--no-video` | music only |
| `--start 60 --length 20` | play one part |

## Catches

- **Every frame is a flash write** on the keyboard. A full run at 5 fps is about 920 writes,
  since frames where nothing changes are skipped. Flash wears out after many writes (typically
  10k to 100k erase cycles; the rating for this chip is unknown). Don't loop it all day.
- **The keys flash** a little on every frame. The keyboard does that when it saves a picture, and
  it can't be hidden. Switching between two picture slots made it worse (`--double`).
- **After a full run, typing can lag.** Unplug and replug the keyboard to fix it.
- It's 63 keys, so the picture is very blocky.

## Files

- `slideshow.py`: the per-key slideshow (the main thing).
- `play.py`: a simpler version where the whole board brightens and darkens with the video
  (one colour for all keys, 30 fps, no flash writes).
- `nd63.py`: the hidraw transport, identify, LED mode save/restore, and probes.
- `gif.py`: the ND63 key map and layout, frame building, and a text preview. Its upload to the
  animation mode (`gif.py test`) does nothing on the ND63, whose firmware lacks that mode.

## What was tried

| route | result on the ND63 |
|---|---|
| live per-key frames (`0x0F`) | ignored in every light mode |
| stored animation (`0x12`, mode 25) | no such mode in this firmware |
| whole-board screen-sync colour (`0x0E`, mode 21) | works, 30 fps: `play.py` |
| custom image re-upload (`0x0C`, mode 13) | works, flashes, wears flash: `slideshow.py` |

Only these commands are ever sent: `0x07`/`0x87` (LED mode), `0x8F` (identify), `0x0C` (image),
`0x0E` (screen colour), `0x0F` (live frame), `0x12` (animation). Never the flash-erase or bootloader
commands.

## Credits

Protocol details come from other people's reverse engineering:

- [sharkfin](https://github.com/dniminenn/sharkfin): protocol notes, image upload, flash wear warnings.
- [monsgeek-akko-linux](https://github.com/echtzeit-solutions/monsgeek-akko-linux): command table,
  the extracted vendor web app, device list, and key matrices.
- [canvas-rgb](https://github.com/iAmChumby/canvas-rgb) (Apache-2.0): the live `0x0F` frame
  layout. `frame_reports` and its self-test in `nd63.py` are adapted from its `tools/kbd-map.py`.

The video is not included. Bad Apple!! PV is by Anira (あにら), the song by Alstroemeria Records,
based on Touhou Project by ZUN.

## License

MIT, see [LICENSE](LICENSE). Not affiliated with IROK, RongYuan or any keyboard brand.
