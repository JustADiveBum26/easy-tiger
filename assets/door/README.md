# The password opening: pictures and versions

The opening you see after typing the password is a door that swings open. It has been through a few versions. Every one is saved, so none of this is lost.

## What the page uses right now (version 7: the engraved gold tiger)

| File | What it is |
|---|---|
| `door-wood.jpg` | A real photo of old wooden planks, re-lit, made to repeat seamlessly so it fills any screen. |
| `shutter.jpg` | The plain wooden slider that covers the peephole. |
| `tiger-engraved.jpg` | The tiger behind the peephole: the engraved gold tiger from the Easy Tiger logo, cut to the peephole's shape and lit like a gold-leaf print in lantern light. Its eyes sit at 33.2% and 66.8% across, halfway down. This is the "2b" option from the comparison sheet. |

## Kept as choices and for reference, not shown right now

| File | What it is |
|---|---|
| `tiger-ai-2.jpg` | The AI tiger that was live in version 6 (Bradley found it cheesy). |
| `tiger-ai-1.jpg` | AI tiger 1: the biggest, brightest eyes (eyes at 27% and 73%). |
| `tiger-ai-3.jpg` | AI tiger 3: the darkest, most menacing (eyes at 29.8% and 70.3%). |
| `ai-originals/` | The full-size pictures as they came out of Copilot (they have a small "Made with AI" badge, which is cropped out of the cuts above). |
| `tiger-eyes.jpg` | A real photo of a tiger's eyes (version 3 and 4). |

To use a different AI tiger, ask Claude: "use AI tiger 1". It changes the picture name and the blink positions.

The side-by-side comparison of the options Bradley chose from (the original eyes, refined glow eyes, the engraved tiger in two lightings, Art Deco line-art eyes, and a minimal gleam) is saved as `peephole-options.png` in the Easy Tiger Misc folder.

## The versions (each one is a bookmark, called a git tag)

| Tag | What it looked like |
|---|---|
| `opening-v1-glowing-slot` | The first one, about 4.7 seconds: a glowing slot, the tiger emblem, curtains part. |
| `opening-v2-css-door` | A door drawn in CSS with straps, a knocker, a brass hatch and glowing CSS tiger eyes. About 8 seconds. The "cartoon" one. |
| `opening-v3-hardware-door` | A photographed wood door with drawn brass hardware, and the real tiger photo behind the hatch. |
| `opening-v4-photo-tiger-fullscreen` | A full-screen plank door with no hardware, and the real tiger photo behind a plain peephole. |
| `opening-v5-original-css-eyes` | The same full-screen door with the original glowing CSS eyes (slit pupils) instead of a picture. |
| `opening-v6-ai-tiger` | The same door with an AI-made tiger (picture 2) behind the peephole. |

To look at one: `git show opening-v2-css-door:css/style.css`
To go back to one, ask Claude: "bring back the opening from opening-v3-hardware-door". It copies only the opening's pieces (the gate box in `index.html`, the opening block at the end of `css/style.css`, and the opening part of `js/main.js`) and leaves everything else as it is. Copying whole files back would also undo later changes like the rules and the menu.

## How the pictures were made

The recipes are in `tools/door-pictures/`:

- `fetch_sources.py` downloads the free source pictures.
- `build_door_v4_plain.py` makes `door-wood.jpg` and `shutter.jpg` (the current ones).
- `make_tiger_eyes.py` makes `tiger-eyes.jpg`.
- `make_engraved_tiger.py` makes `tiger-engraved.jpg` (the current tiger) from the logo.
- `build_door_v3_hardware.py` makes the old hardware door (`door-leaf.jpg`, `jamb.jpg`) for reference.

Results go to `tools/door-pictures/output/` so running a recipe never overwrites what the site uses.

## Credits (all free to use, no conditions)

- Wood door texture "Wooden Gate" and iron plate texture "Metal Plate 02": Poly Haven, https://polyhaven.com (CC0).
- Tiger photo "Tiger fangs": Jessica Weiller, via Unsplash and Wikimedia Commons (CC0), https://unsplash.com/photos/LmVSKeDy6EA.
