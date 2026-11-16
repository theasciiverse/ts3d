# Changes for upstream

Hi! These are the small changes the Asciiverse build of Thing Shooter 3D
carries, written so each can be taken on its own or left out. PATCHES.md
has the full list with the packaging files.

## 1. The keyboard on the first run

In `ensure_file()` (`src/util.c`), the directory case does
`fd = mkdir(path, 0775)` and later `close(fd)`. `mkdir()` returns 0 on
success, so the run that creates `~/.ts3d` closes standard input. The log
file opened next becomes descriptor 0, curses reads its keys from it, and
the menu ignores every key until the game is started again. Returning
`mkdir(path, 0775) ? -1 : 0` straight away for a new directory fixes it.

## 2. A portable install: data beside the binary

When `TS3D_ROOT` is unset and a `data` folder sits beside the executable,
`default_file()` now uses it, and puts `state.json` and `log` in the
per-user state folder (`$XDG_STATE_HOME/ts3d`, else
`~/.local/state/ts3d`, or `%LOCALAPPDATA%\ts3d` on Windows). The
executable is found with `/proc/self/exe` on Linux,
`_NSGetExecutablePath()` on macOS and `GetModuleFileNameA()` on Windows,
else from `argv[0]` when it names a folder (`set_exe_path()`, called from
`main()`). Every override (`TS3D_ROOT`, `TS3D_DATA`, `TS3D_STATE`,
`TS3D_LOG`, `-d`, `-s`) still wins, and an install without data beside
the binary behaves exactly as before. It lets the game run from an
unpacked archive with no installer, as the Windows zip nearly does
already.

Thank you for Thing Shooter 3D!
