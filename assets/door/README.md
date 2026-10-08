# The password opening: pictures and versions

The opening you see after typing the password is a door that swings open. It has been through a few versions. Every one is saved, so none of this is lost.

## What the page uses right now (version 4 with the original eyes)

| File | What it is |
|---|---|
| `door-wood.jpg` | A real photo of old wooden planks, re-lit, made to repeat seamlessly so it fills any screen. |
| `shutter.jpg` | The plain wooden slider that covers the peephole. |

The glowing tiger eyes are drawn in CSS (they are the original eyes from the first door), so they need no picture.

## Kept for reference, not shown right now

| File | What it is |
|---|---|
| `tiger-eyes.jpg` | A real photo of a tiger's eyes (cropped and re-lit), used behind the peephole in versions 3 and 4. Bradley chose to go back to the original glowing eyes. |

## The versions (each one is a bookmark, called a git tag)

| Tag | What it looked like |
|---|---|
| `opening-v1-glowing-slot` | The first one, about 4.7 seconds: a glowing slot, the tiger emblem, curtains part. |
| `opening-v2-css-door` | A door drawn in CSS with straps, a knocker, a brass hatch and glowing CSS tiger eyes. About 8 seconds. The "cartoon" one. |
| `opening-v3-hardware-door` | A photographed wood door with drawn brass hardware, and the real tiger photo behind the hatch. |
| `opening-v4-photo-tiger-fullscreen` | A full-screen plank door with no hardware, and the real tiger photo behind a plain peephole. |

To look at one: `git show opening-v2-css-door:css/style.css`
To go back to one, ask Claude: "bring back the opening from opening-v3-hardware-door". It copies only the opening's pieces (the gate box in `index.html`, the opening block at the end of `css/style.css`, and the opening part of `js/main.js`) and leaves everything else as it is. Copying whole files back would also undo later changes like the rules and the menu.

## How the pictures were made

The recipes are in `tools/door-pictures/`:

- `fetch_sources.py` downloads the free source pictures.
- `build_door_v4_plain.py` makes `door-wood.jpg` and `shutter.jpg` (the current ones).
- `make_tiger_eyes.py` makes `tiger-eyes.jpg`.
- `build_door_v3_hardware.py` makes the old hardware door (`door-leaf.jpg`, `jamb.jpg`) for reference.

Results go to `tools/door-pictures/output/` so running a recipe never overwrites what the site uses.

## Credits (all free to use, no conditions)

- Wood door texture "Wooden Gate" and iron plate texture "Metal Plate 02": Poly Haven, https://polyhaven.com (CC0).
- Tiger photo "Tiger fangs": Jessica Weiller, via Unsplash and Wikimedia Commons (CC0), https://unsplash.com/photos/LmVSKeDy6EA.
