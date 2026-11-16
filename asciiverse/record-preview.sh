#!/bin/sh
# Records the catalog preview, asciiverse/ts3d.cast (hub/RECORDING.md):
# the spinning title, then The Pond (two frogs among the lily pads) and
# the walls and goblins of Entrance, then back to the menu and out.
# asciinema records a tmux pane (own socket, no status line, no bell, no
# user config) that asciiverse/drive.py reads and plays into. A fresh
# state folder, so The Pond is played first. Needs asciinema 3 and tmux.
#   asciiverse/record-preview.sh build/linux/ts3d
set -eu
binary=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
here=$(cd "$(dirname "$0")" && pwd)
out=$here/ts3d.cast
home=$(mktemp -d)
trap 'tmux -L avrec kill-server 2>/dev/null; rm -rf "$home"' EXIT
mkdir "$home/bin"
cp "$binary" "$home/bin/ts3d"
cp -R "$(dirname "$binary")/data" "$home/bin/data"
cd "$home"  # nothing in the recording names a local path
unset TS3D_ROOT TS3D_DATA TS3D_STATE TS3D_LOG
export HOME="$home" XDG_STATE_HOME="$home/state" PATH="$home/bin:$PATH" \
  USER=player LOGNAME=player TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8
tmux -L avrec -f /dev/null new-session -d -s rec -x 100 -y 30 "ts3d" \; \
  set -g status off \; set -g bell-action none \; set -g visual-bell off
python3 -I "$here/drive.py" avrec rec 1 2 &
drive=$!
asciinema rec --headless --overwrite -q \
  --window-size 100x30 --idle-time-limit 2 \
  --capture-env "TERM,COLORTERM,LANG" --title "Thing Shooter 3D" \
  --command "tmux -L avrec attach -t rec" "$out"
wait "$drive"
