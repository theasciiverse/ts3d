# Thing Shooter 3D

**Kill the enemies before they kill you. Luckily, they aren't very smart.**

You start on the sand beside a pond, under a wide cyan sky, with lily
pads on the water and two frogs coming your way. Swing round, line them
up and fire: your shots are slow red bolts that burst where they land,
and whatever you kill leaves a pale spirit rising into the air.

Thing Shooter 3D is a first-person shooter drawn entirely in your
terminal. Walls, sand, sky and every creature are coloured characters,
rendered in real 3D by a ray-casting engine its author wrote himself.
Ten levels open one after another: The Pond, the cave mouth of
Entrance, the lettered walls of Gobstopper and Halls, Columns and All
Sides with goblins a touch faster than you, Dance Off and Double Trouble
with demons that hurl flaming skulls, Ensemble with everyone at once,
and Medley, where a giant eye backs away from you spitting frogs, then
bats, then goblins, then demons.

Your bullets are slow, so lead your shots, or shoot theirs out of the
air. The walking keys switch walking on and off, so you can set off
sideways and keep both hands for aiming. The bigger your terminal, the
easier the game gets; 80x24 works.

## Playing

Run `ts3d` from this folder, with its `data` folder beside it. Choose
Levels, then a level; each one you win opens the next.

- **W**, **A**, **S**, **D**: walk forward, left, back or right; press
  again to stop
- **Q** and **E**: turn left and right
- **Space**: shoot; hold **Shift** or turn on **Caps Lock** to shoot
  while you walk and turn
- **P**: pause; **X**: leave the level
- In the menus: **W** and **S** or the arrows to move, **D** or **Enter**
  to choose, **A** or **Esc** to go back; Help and About are there too

The levels you have won are kept in `state.json`, and a log of the last
session in `log`, in the state folder: `$XDG_STATE_HOME/ts3d`, else
`~/.local/state/ts3d`, or `%LOCALAPPDATA%\ts3d` on Windows.
`ts3d -h` lists the options and the variables that move them.

## Making your own

Everything in `data` is plain text. Each texture is a text file in which
every character is one pixel's colours; creatures, levels and menus are
JSON. `data/README` documents every format, so you can repaint a frog
or build a level of your own.

## Credits

- Thing Shooter 3D: Jude Melton-Houghton (TurkeyMcMac), art, game
  design and programming, https://github.com/TurkeyMcMac/ts3d (MIT, see
  LICENSE), with his own d3d renderer and json parser
- This package: Asciiverse, for the av launcher and the catalog at
  https://asciiverse.sh. What we changed is in PATCHES.md.

## Building

`sh asciiverse/build.sh` builds `build/<platform>/ts3d` with `data`
beside it: statically against ncurses on Linux (in Alpine for the
release), against the system curses on macOS, and with MinGW and static
PDCurses in MSYS2 on Windows. The release workflow
(`.github/workflows/asciiverse-release.yml`) builds all three. The
upstream README covers the Makefile, the tests and the `texture` viewer.
