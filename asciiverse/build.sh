#!/bin/sh
# Builds Thing Shooter 3D for the Asciiverse catalog. Leaves the binary in
# build/<platform>/ts3d (ts3d.exe on Windows); the game's data/ folder
# ships beside it.
#   Linux:   docker run --rm -v "$PWD":/src -w /src alpine:3.22 sh asciiverse/build.sh
#            (fully static against Alpine's ncurses; reads the system's
#            terminfo). Elsewhere it links static against the host's
#            ncursesw and tinfo.
#   macOS:   sh asciiverse/build.sh  (links the system's curses)
#   Windows: sh asciiverse/build.sh  in an MSYS2 UCRT64 or CLANGARM64 shell
#            with pdcurses installed (static PDCurses, as upstream's
#            make-windows does with MinGW)
#
# The flags are the Makefile's own (C99, POSIX 2001); only the curses
# library and the output path differ per platform.
set -eu
case "$(uname -s)" in
  Linux)  platform=linux ;;
  Darwin) platform=macos ;;
  MINGW*|MSYS*|UCRT*|CLANG*) platform=windows ;;
  *) echo "unknown platform $(uname -s)" >&2; exit 1 ;;
esac

if [ -f /etc/alpine-release ]; then
  apk add --no-cache build-base ncurses-dev ncurses-static >/dev/null
fi

out=build/$platform
mkdir -p "$out"
cflags="-std=c99 -O2 -Wall -Wextra -Wpedantic -D_POSIX_C_SOURCE=200112L -DJSON_WITH_STDIO"
version=$(cat version)

case $platform in
  linux)
    # Alpine's libncursesw.a has terminfo built in; elsewhere it is libtinfo
    libs="-static -lncursesw -lm"
    [ -f /etc/alpine-release ] || libs="-static -lncursesw -ltinfo -lm"
    exe=$out/ts3d ;;
  macos)
    libs="-lcurses -lm"
    exe=$out/ts3d ;;
  windows)
    # MSYS2 installs PDCurses' header as pdcurses.h; the game includes
    # <curses.h>, so a one-line header points it there.
    mkdir -p build/win-include
    printf '#include <pdcurses.h>\n' > build/win-include/curses.h
    cflags="$cflags -Ibuild/win-include"
    libs="-static -lpdcurses -lm"
    exe=$out/ts3d.exe ;;
esac

${CC:-cc} $cflags -DTS3D_VERSION="\"$version\"" -o "$exe" src/*.c $libs
strip "$exe"
rm -rf "$out/data"
cp -R data "$out/data"
echo "built $exe"
