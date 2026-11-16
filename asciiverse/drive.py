"""Plays Thing Shooter 3D for the catalog preview (asciiverse/record-preview.sh).

Reads the tmux pane with its colours and presses keys at a watchable pace.
In a level it looks above the horizon for anything that is not sky or
wall, turns toward it (q / e) and fires (Space) once it is in the
middle, stepping forward (w) now and then when nothing is in sight.
Levels are picked from the menu by their number.
    python3 -I drive.py <tmux socket> <session> <level number>... [--debug]
"""
import re
import subprocess
import sys
import time

SOCK, SESS = sys.argv[1], sys.argv[2]
LEVELS = [a for a in sys.argv[3:] if a.isdigit()]
DEBUG = "--debug" in sys.argv
T0 = time.time()
LEVEL_TIME = 24.0
SGR = re.compile(r"\x1b\[([0-9;]*)m|([^\x1b])")


def tmux(*args):
    return subprocess.run(["tmux", "-L", SOCK, *args], capture_output=True,
                          text=True).stdout


def log(*a):
    if DEBUG:
        print(round(time.time() - T0, 1), *a, file=sys.stderr)


def grid():
    """The pane as rows of (char, background colour 0 to 7)."""
    rows, bg = [], 0
    for line in tmux("capture-pane", "-p", "-e", "-t", SESS).split("\n"):
        row = []
        for m in SGR.finditer(line):
            if m.group(1) is not None:
                for p in (m.group(1) or "0").split(";"):
                    p = int(p or 0)
                    if p == 0:
                        bg = 0
                    elif 40 <= p <= 47:
                        bg = p - 40
            else:
                row.append((m.group(2), bg))
        rows.append(row)
    return rows


def text(rows):
    return "\n".join("".join(c for c, _ in r) for r in rows)


def key(k, wait=0.12):
    log(k)
    tmux("send-keys", "-t", SESS, k)
    time.sleep(wait)


def target(rows):
    """How far the nearest thing is from the middle (0 when the middle
    column is on it, else its centre's offset) and how wide it is; None
    when nothing is seen. A thing is a run of cells around the horizon
    that differ from the commonest colour of their row; red is left out,
    since the player's own bullets fly off in red."""
    w = max((len(r) for r in rows), default=0)
    if w < 20 or len(rows) < 10:
        return None
    mid = w // 2
    horizon = len(rows) // 2
    band = range(3, horizon + 3)
    count = [0] * w
    for y in band:
        row = rows[y]
        colours = [bg for c, bg in row if c == ":"]
        if not colours:
            continue
        common = max(set(colours), key=colours.count)
        for x, (c, bg) in enumerate(row):
            if c == ":" and bg != common and bg != 1:
                count[x] += 1
    cols = [x for x in range(w) if 2 <= count[x] < len(band) - 2]
    blobs, cur = [], []
    for x in cols + [None]:
        if cur and (x is None or x - cur[-1] > 2):
            if len(cur) >= 2:
                blobs.append(cur)
            cur = []
        if x is not None:
            cur.append(x)
    if not blobs:
        return None
    best = min(blobs, key=lambda b: abs((b[0] + b[-1]) / 2 - mid))
    width = best[-1] - best[0] + 1
    if best[0] + 1 <= mid <= best[-1] - 1:
        return 0, width
    return (best[0] + best[-1]) / 2 - mid, width


def play_level(n):
    key("Home", 0.4)
    key("1", 0.3)
    key("d", 0.6)                 # Levels
    key(str(n), 0.4)
    key("d", 1.5)                 # into the level
    start = time.time()
    moving = ""                   # the movement key toggled on, if any

    def move(k):
        nonlocal moving
        if k == moving:
            return
        key(k or moving, 0.04)    # a new direction, or the same to stop
        moving = k

    while time.time() - start < LEVEL_TIME:
        rows = grid()
        t = text(rows)
        if "Press Y" in t:          # won, or died
            move("")
            time.sleep(2.0)
            key("y", 1.2)
            return "YOU WIN" in t
        if "TARGETS LEFT" not in t:  # back in the menu
            return False
        seen = target(rows)
        log("seen", seen)
        if seen is None:
            # look around, and wander a little
            move("w" if int(time.time() - start) % 6 < 2 else "")
            key("e", 0.15)
            continue
        off, width = seen
        if abs(off) > 10:
            move("")
            key("q" if off < 0 else "e", 0.1)
        elif off:
            move("d" if off > 0 else "a")   # sidestep onto it
            time.sleep(0.05)
        else:
            move("w" if width < 10 else "")
            key("Space", 0.1)
    key("x", 1.0)                 # leave the level
    key("y", 1.0)
    return False


time.sleep(3.0)                    # the title screen
for n in LEVELS:
    play_level(n)
key("Home", 0.5)
time.sleep(1.5)
key("x", 0.5)
