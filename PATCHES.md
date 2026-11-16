# Changes from upstream

This is the Asciiverse packaging of [Thing Shooter 3D](https://github.com/TurkeyMcMac/ts3d)
by Jude Melton-Houghton (MIT, `LICENSE`), a first-person shooter drawn in
the terminal. Upstream is the `upstream` remote; this build is upstream's
`master` at `8c52e9c` (2022-10-17), which is its `v1.16.2` tag. The
`asciiverse` branch carries the changes below, each small enough to offer
upstream (UPSTREAM.md).

## The game

Unchanged: the same ten levels, creatures, textures, menus and texts in
`data/`, and the same rules and controls.

## Code

- **Data beside the binary, state in the state folder** (`src/util.c`,
  `src/util.h`, `src/main.c`): upstream finds everything through
  `TS3D_ROOT`, else `~/.ts3d` (`%AppData%\ts3d` on Windows), and expects
  the data to be installed there. Now, when `TS3D_ROOT` is unset and a
  `data` folder sits beside the executable (found through
  `/proc/self/exe`, `_NSGetExecutablePath` or `GetModuleFileName`, else
  `argv[0]`), the game reads its data from there, and keeps `state.json`
  (the levels won) and its `log` in `$XDG_STATE_HOME/ts3d` (else
  `~/.local/state/ts3d`, or `%LOCALAPPDATA%\ts3d` on Windows), creating
  the folder. `TS3D_ROOT`, `TS3D_DATA`, `TS3D_STATE`, `TS3D_LOG`, `-d`
  and `-s` still win, and an install with no data beside the binary
  keeps upstream's `~/.ts3d`. The `-h` text says so.
- **The keyboard on the first run** (`src/util.c`): `ensure_file()` took
  `mkdir()`'s return value of 0 for a file descriptor and closed it, so
  the run that created the game's folder closed standard input. The log
  then opened as descriptor 0, curses read its keys from the log file,
  and no key did anything until the game was started a second time. A
  new directory now returns at once.

## Build settings

`asciiverse/build.sh`, not the Makefile, builds the release, with the
Makefile's own flags (`-std=c99 -D_POSIX_C_SOURCE=200112L
-DJSON_WITH_STDIO`, plus `-O2`):

- Linux links ncurses statically in Alpine (`-static -lncursesw`), so the
  binary needs nothing installed; it reads the system's terminfo. macOS
  links the system curses. Windows links PDCurses statically in MSYS2's
  MinGW, as upstream's `make-windows` does; MSYS2 names the header
  `pdcurses.h`, so the build writes a one-line `curses.h` pointing at it
  into `build/`.
- The binary goes in `build/<platform>/` with a copy of `data/` beside it.

## Packaging

- `asciiverse/build.sh` (new): the build above.
- `.github/workflows/asciiverse-release.yml` (new): av archives for Linux
  (static, x86-64 and ARM64), macOS (Intel and Apple silicon) and Windows
  (x86-64 and ARM64), each the binary with its `data/` folder, plus
  SHA256SUMS, on a `*-av.*` tag. The Windows jobs are written but have
  not run yet.
- `asciiverse/README.md` (new): the README in each archive.
- `asciiverse/record-preview.sh`, `asciiverse/drive.py` (new): the
  catalog preview.
- `asciiverse/ts3d.toml`, `asciiverse/ts3d.md`, `asciiverse/ts3d.cast`
  (new): the catalog manifest, store page and preview, as drafts for hub.
- `CLAUDE.md`, `PATCHES.md`, `UPSTREAM.md` (new): notes; `.gitignore`
  leaves out `build/`.
