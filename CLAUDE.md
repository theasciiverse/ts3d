# Thing Shooter 3D (Asciiverse packaging)

Jude Melton-Houghton's Thing Shooter 3D (C, curses, MIT), packaged for
the Asciiverse catalog (id `ts3d`, kind `game`, genre `action`). Not our
code: the game stays as its author made it; list every change in
PATCHES.md and keep each one offerable upstream (UPSTREAM.md).

- `upstream` is github.com/TurkeyMcMac/ts3d (branch `master`); ours is
  branch `asciiverse`, `origin` github.com/theasciiverse/ts3d (private).
- Build: `sh asciiverse/build.sh` (Linux static in alpine:3.22 under
  docker in CI; locally it links static against the host's ncursesw and
  tinfo). Binary in `build/<platform>/ts3d` with `data/` beside it; the
  game finds its data there when `TS3D_ROOT` is unset.
- Release: tag `v<upstream version>-av.<n>` (first `v1.16.2-av.1`) and
  push it; `.github/workflows/asciiverse-release.yml` builds Linux, macOS
  and Windows (the Windows jobs have not run yet).
- `state.json` (levels won) and `log` live in `$XDG_STATE_HOME/ts3d`.
  Tests and scripted runs always set a scratch `XDG_STATE_HOME` and
  `HOME` in the same command, unset `TS3D_ROOT`, and run under
  `systemd-run --user --scope -p MemoryMax=4G`. The game beeps on hits:
  tmux sessions get `bell-action none`.
- Preview: `asciiverse/record-preview.sh build/linux/ts3d` (100x30).
- Catalog drafts: `asciiverse/ts3d.toml` and `.md`; copies go in
  hub/catalog, the cast in hub/site/casts.
