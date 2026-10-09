# Easy Tiger Website: Handshake

Read this first. It is the main primer for everything in this project, and it was rewritten on Oct 9, 2026 to match what actually exists. If something here is out of date, tell Bradley and fix it. Keep it current: when a decision changes or a piece gets finished, update the right section (don't just add a line at the bottom).

---

## HARD RULES (never break these)

1. **Never access, read, open, list the contents of, copy, or use ANY file inside a folder that is marked "(DO NOT USE)" or named like "DO NOT USE".** Bradley uses these folders to park things he has rejected. This applies to every folder on his computer, now and in the future. Don't peek to "check what's in there", don't use it for comparing duplicates, don't copy from it. If a task seems to need something from such a folder, stop and ask him. Example today: `Easy Tiger Construction/DO NOT USE/`.
2. **Never use the "Archived" folders either** (for example `Easy Tiger Menus/Archived Menus/`, `Easy Tiger Logo/Archived Version/`). Bradley said they hold historical versions and must not be used unless he says so. Use only the newest files outside the archives.
3. **Never write the Knock to Enter password words anywhere** (not in files, not in notes, not in commit messages, not in comments, not on printed signs). Only the scrambled fingerprint goes in `js/firebase-config.js`. Don't write anything about what the words are, look like, or relate to. Same for the house password and the admin's email: they live only in Firebase.
4. **Never `git add` a whole folder** (like `assets`). Add specific files by name, then check `git status` before committing. A QR folder was published by mistake once this way.
5. **The repo is public.** No passwords, keys, home address, phone numbers, personal emails, guests' info, or anything private in any file. Commits must use the GitHub noreply email (already set in this repo's git config), never Bradley's real email.
6. **Ask before** creating or changing any account or cloud setting, spending or committing money, deleting anything, rewriting git history, or force-pushing.
7. **Don't touch his source folders** (Construction, Menus, Logo, Misc). Read the newest files in them, never edit, move, or delete them.

---

## What we're building

A small, private-feeling website for **Easy Tiger**, the speakeasy room Bradley is building in his basement in Columbia, Missouri. A fun, moody, 1920s Prohibition-style site that guests reach by link only (no domain, no search listing). The name is a Mizzou Tigers nod. The room is a place to unplug after a long day: no phones, no screens, bottles meant to be opened and shared, not saved.

## Where things live (live now)

| What | Where |
|---|---|
| The website | https://justadivebum26.github.io/easy-tiger/ (GitHub Pages, serves the `main` branch root; every push updates it in about a minute) |
| Short link | https://tinyurl.com/EasyTigerCoMo (Bradley made it; upper and lower case both work; points at the address above) |
| Hidden admin page | https://justadivebum26.github.io/easy-tiger/admin.html (not linked anywhere; Google sign-in) |
| The repo | https://github.com/JustADiveBum26/easy-tiger (public) |
| Firebase project | `easy-tiger-como` (Firestore in `nam5`). Separate from his `family-hub` project, which must never be touched. |
| Photo storage | Cloudinary cloud `czj4oq2l`, unsigned upload preset `easy-tiger-guests` (folder `easy-tiger`) |
| Printed sign and QR codes | `assets/qr/` on his computer only (git-ignored, not on the site) |

Tools installed on his PC during this work: GitHub CLI (`gh`, logged in as JustADiveBum26), `firebase-tools` (logged in), and Python packages for testing and pictures (playwright, pillow, opencv, pymupdf, python-docx, segno, zxing-cpp). Local Chrome is at `C:\Program Files\Google\Chrome\Application\chrome.exe`.

---

## Who you're working with

Bradley Jenkins. How he likes to work:

- **Casual tone, plain words.** No big words, no long winding sentences. Talk like a normal person.
- **Ask questions before big decisions.** Short, clear ones. Don't guess on anything that costs money, touches accounts, or is hard to undo.
- **Explain as you go.** One or two plain sentences on why.
- **He is comfortable with GitHub and Firebase** but is not a front-end developer. Keep setup simple.
- **Anything written for the site should sound like a person wrote it.** Plain, warm, a little dry. No filler, no buzzwords, go easy on em dashes.
- **He gives fast, specific feedback and changes his mind.** Show options side by side when taste is involved. Keep everything he rejects saved (git tags, kept files) so it can come back.
- **He wants it to look high end and classy**, never cheesy. Fake-looking details (cartoon hardware, cat-like eyes, AI-looking pictures) got rejected.
- **Most guests use phones.** Check every change at phone width first (360x640 and 390x844), then a computer.

### Working arrangement (as of Oct 9, 2026)

He authorized Claude to set up the GitHub repo, Pages, and the Firebase project. Since then Claude has made changes, tested them, and **published each batch**, then reported what went live, and he went along with that (he said he'd send "lots of minor updates"). Keep doing that for ordinary site changes, but still ask first for anything in HARD RULE 6. Always run the tests below before publishing, and verify the live site after.

---

## Folders

Outside the repo, in `Downloads\Easy Tiger Project\` (Bradley's, read-only for Claude, newest files only, see the hard rules):

- `Easy Tiger Logo\` (use `Version 8`, the newest; `Archived Version` is off limits). The page uses `02_Easy_Tiger_HERO_Black_Background_5000px.png`.
- `Easy Tiger Menus\` (newest Word menu: `Easy Tiger Spirits Menu10082026v2.docx`; `Archived Menus` is off limits).
- `Easy Tiger Construction\` (his build photos; `DO NOT USE` inside it is off limits).
- `Easy Tiger Misc\` (holds `peephole-options.png`, the side-by-side of the opening options).
- `Easy Tiger Webpage\` is the repo (this folder).

Inside the repo:

```
index.html              the whole front page (one long page with anchor links)
admin.html              hidden admin page (approve/delete photos and guest notes)
robots.txt, manifest.webmanifest
css/style.css           all styling (plain CSS, no build step)
js/main.js              menu + search, guest book, photo wall, nav dropdown, Knock to Enter gate, opening, scroll-to-top
js/admin.js             admin page
js/store.js             the DEMO store (browser-only). Dormant when Firebase is configured.
js/store-firebase.js    the REAL store (Firestore + Cloudinary), replaces EasyStore when configured
js/firebase-config.js   public connection values + the Knock to Enter fingerprint (no secrets)
js/menu-data.js         the 110 drinks, generated from the Word menu (see "Updating the menu")
firestore.rules, firebase.json   database security rules
assets/logo, build, menu, icons, social, door    pictures and the menu PDF
assets/qr/              printable QR codes and sign (git-ignored)
tools/                  make-menu-data.py, make-knock-hash.py, door-pictures/ (picture recipes)
CLAUDE.md               this file (see "Open decisions": it is publicly served)
```

Always bump the `?v=NN` cache number on the CSS/JS links in `index.html` and `admin.html` when changing those files, so phones don't keep old copies (currently `?v=32`).

---

## The page, top to bottom

Order matters: the top menu follows the same order.

1. **Knock to Enter gate** (full-screen, before the page). See "The gate and the opening".
2. **Nav bar.** Small tiger + EASY TIGER. Links, in order: House Rules, Drinks, The Story, The Build, Guest Book, Photos, Extras. On screens 1000px wide and under it becomes a gold three-line button (icon only, no word "Menu", on purpose) that drops a solid list; it closes on link tap, outside tap, Escape, logo tap, or widening.
3. **Hero.** Logo between burgundy velvet curtains with a gold rod. Line: "Put the phone down. Stay a while." **No buttons** (he removed them).
4. **Gold band.** "Speak softly · Pour generously · Stay late". This is still the original placeholder; he hasn't commented. Now overlaps with rule 5 (Stay Late(ish)), so ask before leaving it.
5. **House Rules** (`#rules`). Framed poster, Roman numerals I to V, bold headline plus an italic line. Final wording:
   1. Phones Off. Conversation On. / Be in the Moment.
   2. Drink It, Don't Save It. / It's Here to Drink, Not Look At.
   3. Pour a Little for Your Neighbor. / An Empty Glass Is Everyone's Problem.
   4. Leave Your Bad Day at the Door. / Pick It Back Up on the Way Out.
   5. Stay Late(ish). / The More We Like You, the Later We're Open.
6. **Drinks** (`#drinks`, heading "Spirits Menu"). A search box, then a card "Pick a pour" listing the seven types with counts. See "Updating the menu".
7. **The Story** (`#story`). **Currently Latin filler text only** (he doesn't want anything real showing yet), in the same layout, plus the "In the room" box also with filler. Real wording is in git history (commit `a6c7e1b` and earlier). Put real text back only when he asks.
8. **The Build** (`#build`). 13 photos in a centered gallery, **no captions** (he asked), alt text only. Files in `assets/build/` (01 to 06 are 1600px; 00, 02b, 03b, 04b, 05b, 05c, 05d are 640px). Two show the storage area behind the wall, uncropped on purpose (he said no). Two show a person.
9. **Guest Book** (`#guestbook`). Name, note, house password, "Sign it". Entries need his approval before they show.
10. **Photo Wall** (`#photos`). Add a photo, an approval note, a grid of approved photos in gold frames.
11. **Extras** (`#extras`). One card: Pours We Remember (empty, placeholder).
12. **Footer.** "Easy Tiger · Columbia, Missouri · Tagline goes here" (placeholder; he dislikes the old "Keep it between us").

The page always opens at the very top (no remembered scroll position, `#section` stripped from the address, jump to top after the opening). Don't undo this without asking.

### About the room (the real details, for when the Story comes back)

Use only what's listed. Don't invent details. Never put the street address on the site.

- Deep teal green walls (Sherwin-Williams Cascades), flat black ceiling with pipes, ducts and joists painted black
- One wall of burned cedar (shou sugi ban): black charcoal with silver-grey grain, not honey colored
- Red leather sofa against the cedar wall, two brown Chesterfield chairs facing it, a hammered copper and bronze round coffee table, a vintage-looking rug with two tigers
- Gold fixtures and warm amber Edison light only, no cool white light
- Exposed concrete floor, cleaned and sealed
- A burgundy velvet curtain where a door would be
- Prohibition-era art prints and gold animal busts on one wall, a record player on a dark walnut console

---

## Design

Dark, moody, classy 1920s speakeasy. Art Deco. Gold foil on black, velvet, pinstripes, double-line frames.

| Use | Color |
|---|---|
| Gold (from the logo) | `#d4a846` (CSS variable `--gold`) |
| Page background | `#070908` |
| Teal sections | `#0d1917` |
| Burgundy section | `#2a0d15` |
| Velvet curtains | `#3d0f1a`, `#5a1626`, `#2e0a13` |
| Main text, ivory | `#efe6d0` |
| Soft text | `#c9c0a8`, `#a8a08c` |

Fonts (Google Fonts): **Playfair Display** 600 caps with wide spacing for headings, **Cormorant Garamond** for body and italics, **Josefin Sans** small caps for labels and buttons.

Signature touches: gold double-line frames; photos in a thin gold frame with a dark mat; section headers (small gold label, big caps heading, thin gold line with a diamond); pinstripes on teal and burgundy sections; velvet curtains in the hero; logo with `mix-blend-mode: screen` (its background is pure black); no emoji, thin gold line icons. The logo is finished: never redraw or restyle it.

---

## How the features work

### The menu and search
- Source of truth is the **Word menu** in `Easy Tiger Menus`. The 110 drinks are in `js/menu-data.js`: Bourbon 51, Rye 13, Other American Whiskey 8, Tequila 1, Gin 3, Liqueur 7, House Drinks 27. (A `.js` file on purpose: browsers block `fetch()` of `.json` when a page is opened from a folder.)
- The card first shows **only the list of types**. Tapping one opens that type's drinks in a fresh view with an "All types" back button; each drink opens to show notes, age, and mash bill (or "made with"). House Drinks are grouped under base-spirit headings (Bourbon, Rye, Other American Whiskey, Tequila, Gin, Vodka).
- **Search** (box above the card) searches all drinks by name, maker and base first, then tasting notes; ignores caps, accents and apostrophes. Typing opens a Search results view; clearing it goes back to the types.
- **Bradley rejected** tabs plus an always-open list. Don't bring them back.
- "Confirm on bottle" values are hidden on the site. Two tasting notes in the Word file still contain to-do wording (Redwood Empire Lost Monarch, Russell's Reserve 6 Year); he must fix them in Word.
- The PDF `assets/menu/easy-tiger-menu.pdf` is the Word menu saved as PDF (cover still says "Spirits Menu"; Wine isn't on the menu yet).

### The gate and the opening
- **Knock to Enter.** A full-screen gate asks for a password on **every** page load (refresh, new tab, new window, back button). Nothing is remembered. Screen: tiger, "Knock, knock", "Every good speakeasy has a password", "Get it right and the door opens. Get it wrong and, well.", a box, and a button "Try the door". Wrong answers rotate through four short teases and shake the card. Caps, spaces and punctuation don't matter. The check is in the browser against a SHA-256 fingerprint (`knock.hash` in `js/firebase-config.js`), so it is a fun gate, **not security**. An empty hash turns the gate off. `admin.html` is not gated. To change the words: `python tools/make-knock-hash.py "new words"`, paste the result into the config. Choose words that aren't easy to guess, since the fingerprint is public.
- **The opening** (about **11 seconds**) after the right password: a full-screen plank-door scene (real photo wood, no hardware) fades in; two knocks (a double-knock phone buzz on supporting phones); a small peephole's wooden slider opens and the **engraved gold tiger from the logo** looks out (fades up, head turns left then right, a lantern shimmer in the eyes, one soft blink); the doorman says "Let's have a look at you." / "That's the one." / "Mind the stairs."; the slider snaps shut; the door swings open in 3D into warm light; the tiger emblem rises with a gold shine and "Welcome to Easy Tiger", which holds about 3 seconds (the emblem breathes, a second shine); then it fades to the page at the top. **Tap, click or any key skips** (ignored for the first half second so the Enter that sent the password doesn't skip it). People with "reduce motion" get a calm 0.4 s fade.
- The second-by-second timeline is the comment above `.gate-stage` in `css/style.css`. `OPENING_MS = 11000` in `js/main.js` must change together with it.
- Pictures are in `assets/door/` (see its `README.md`): `door-wood.jpg` (seamless plank tile repeated across the whole screen), `shutter.jpg`, `tiger-engraved.jpg` (the one in use; eyes at 33.2% and 66.8% across, halfway down, which is where the glow and blink are placed). Kept but unused: `tiger-eyes.jpg` (real tiger photo), `tiger-ai-1/2/3.jpg` and `ai-originals/` (AI tigers from Copilot), all saved as choices.
- **History of the opening (all rejected or replaced, all saved as git tags):** `opening-v1-glowing-slot` (4.7 s slot), `v2-css-door` (cartoon door with drawn hardware), `v3-hardware-door` (photo door with drawn brass hardware, "cheesy"), `v4-photo-tiger-fullscreen` (real tiger photo), `v5-original-css-eyes` (glowing slit-pupil eyes, read as cat/snake), `v6-ai-tiger`, and current `v7-engraved-tiger`. Other options he saw but didn't pick: brighter engraved tiger, refined CSS glow eyes, Art Deco line-art eyes, a minimal gleam (side by side in `Easy Tiger Misc\peephole-options.png`). To bring a version back, copy only the opening's pieces from the tag (gate box in `index.html`, the opening block at the end of `css/style.css`, the opening part of `js/main.js`), never whole files (that would undo later changes). Don't delete the tags or `assets/door`.
- Picture recipes (tested, they reproduce the site's pictures) are in `tools/door-pictures/`; the engraved tiger needs the logo file path as an argument.

### Guest book, photos, admin
- Everything goes through `window.EasyStore`. `js/store.js` is the demo (browser-only) version; `js/store-firebase.js` replaces it when `js/firebase-config.js` has the project values (it does, so the site runs in real mode).
- **Both guest book entries and photos need Bradley's approval.** Guests write to `guestbookPending` / `photosPending` (add-only, must send the right house password, limits: name 60, note 400, caption 80, images only, 8 MB, photo address must start with `https://res.cloudinary.com/`). Only the admin can read pending items (so the typed password is never public). Approving copies the entry, without the password, into public `guestbook` / `photos`. The house password is the Firestore document `config/house` and the admin is `config/admin`; both were created by Bradley in the Firebase console and nobody can read or write them from a web page. Guests' photos are shrunk to 1400px in the browser (also drops camera data) and uploaded to Cloudinary.
- **Admin page:** Google sign-in, shows waiting photos and notes with Approve and Delete, posted ones with Delete, a summary line, and the waiting count in the tab title like "(3) Easy Tiger · Admin" (refreshes every 2 minutes).
- Redeploy rules: `firebase deploy --only firestore --project easy-tiger-como`.
- Security was tested from outside on Oct 8, 2026: pending items, `config/house` and `config/admin` cannot be read; outsiders cannot write with a wrong password or delete anything.
- **Known limits:** a wrong-password guest's photo file still reaches Cloudinary before Firestore refuses the entry (junk can be removed in the Cloudinary Media Library); Delete on the admin page removes the entry from the site but not the file from Cloudinary.
- **Still needs Bradley's hand test** with the real password and his Google login: post an entry, upload a photo, sign in at admin, approve both, delete both. Not confirmed yet.

### Link preview and home-screen icon
Open Graph tags plus `assets/social/preview.jpg` (1200x630), `assets/icons/*`, and `manifest.webmanifest`. Messaging apps cache previews, so changes can take a while to show.

### QR codes and the printed sign (local only, `assets/qr/`)
Plain and tiger-emblem QR codes and a 6x8 inch print-ready sign (`easy-tiger-sign-6x8-logo-qr.pdf` is the one to print). They encode the direct site address (not the TinyURL, so they survive a TinyURL change). The sign says "Scan to come in", shows `tinyurl.com/EasyTigerCoMo`, and "Then ask for the secret password" (never print the password). All were decoded with a scanner at many sizes, but **not tested on a real phone**. The emblem covers about 10% of the code (30% is the limit); the `*-logo20-*` files (20%) failed every scanner, so ignore them. For prints under about 1.5 inches use the plain code. The sign's bottom line "Keep it between us" is a line Bradley dislikes on the site; ask before reprinting.

---

## How to do common jobs

- **Update the menu:** Bradley edits the Word file. Run `python tools/make-menu-data.py "<path to the newest docx>"` (needs python-docx; it reads formatting: Heading 1 = type, bold 12pt = drink, italic 9.5 = maker/proof or "Built on", italic 9 = age/mash bill, regular 10 = notes). It stops with a message if it can't tell a House Drink's base spirit (add a word to `BASE_WORDS`). Then save the docx as PDF (Word, or Word COM from PowerShell) over `assets/menu/easy-tiger-menu.pdf`, bump the `?v=`, test, publish.
- **Add or change Build photos:** work from copies in his Construction folder (skip anything in a DO NOT USE folder), resize to about 1600px (or keep small ones as they are), re-save as JPEG to drop camera data, put them in `assets/build/`, edit the gallery in `index.html`.
- **Change the gate words:** see above.
- **Swap the tiger behind the peephole:** change the `src` in the `.hatch-tiger` block and the glow/blink percentages (`.tiger-glow-*`, `.tiger-lid-*`) in `css/style.css`; the numbers for each picture are in `assets/door/README.md`.
- **Restore Story text, add Pours We Remember entries, change the tagline or footer:** only when he asks.

### Testing before publishing (always)
Start a local server (`python -m http.server <port>` in the repo folder, stop it afterward) and drive it with Playwright using the local Chrome. Check at **360x640, 390x844 (touch), 1366x768, 1920x1080, 2560x1080**: no sideways scroll, the gate and opening play to the end (about 11 s) and land at the top, tap to skip (about 0.45 s), Enter doesn't skip, reduced motion (about 0.4 s), a wrong password teases and doesn't start the door, a refresh asks again, no console errors, no failed requests, div tags balanced. After pushing, wait for the Pages build to match the commit (`gh api repos/JustADiveBum26/easy-tiger/pages/builds/latest`) and re-test the **live** address.

---

## Decisions Bradley made (so we don't redo them)

- Hosting is GitHub Pages, link only, `noindex` + `robots.txt`. Be honest with him that this is not real security.
- Menu is a PDF plus a clickable list generated from the Word file. Menu naming: nothing called just "Menu" (it clashes with navigation): "Drinks", "Spirits Menu", "Pick a pour".
- No Drink of the Night for now (removed). Held for later: shrinking the 1.2 MB logo, tap-to-enlarge photos, a house-password hint on the forms.
- No captions on Build photos. Photos 3 and 4 stay uncropped.
- Phone navigation is a dropdown opened by an icon. Sections and menu are in the same order.
- The page opens at the top; the gate asks every time; the opening is about 11 s and skippable.
- Rejected looks: cartoon or drawn door hardware, a narrow door on desktop, slit-pupil glowing eyes, real tiger photo, AI tiger pictures. He wants high end and classy; the engraved gold tiger from the logo is the current choice ("keep it for now").

---

## Open items

Waiting on Bradley (don't start unless he brings them up; remind him at natural stopping points):

1. **Hand test** of the real guest book, photos and admin (above).
2. **Story text:** how the idea started and who helped build it. Then restore the real room details.
3. **Footer tagline** (placeholder now) and what to do with the gold band line.
4. **Pours We Remember:** empty; needs entries and a simple way to add them.
5. **Menu cleanup:** fix the two to-do notes in the Word file, then regenerate the list and the PDF. PDF cover still says "Spirits Menu".
6. **Real house password:** he sets it in `config/house` in Firebase. Change it if he used a throwaway for testing.
7. Optional ideas (ask first): a random Prohibition-era quote, "who's coming tonight", a record of the week, a different tiger each visit.

Decisions waiting on him from the Oct 8 audit:

- **`CLAUDE.md` is public** (served at the site address). Recommend keeping it local only (git-ignore it) since it is Claude's working notes. He hasn't answered.
- **Scrubbing old mistakes out of git history** (an old wrong hint in older versions of this file; the QR files that were briefly published): needs a history rewrite and force-push, and moves the `opening-v*` tags. Not urgent, nothing sensitive beyond the hint. Ask first.
- **`assets/door/ai-originals`** (7 MB of unused full-size AI pictures) is published; could be kept local only.
- `js/store.js` still ships the dormant demo store with a demo password (harmless; could be removed).
- One tiny test image (the 96px logo icon) sits in his Cloudinary Media Library; he can delete it.

### Audit result (Oct 8, 2026)
All 53 published files and all saved versions were searched: no emails, phone numbers, street addresses, local folder names, passwords or secrets; every commit uses the noreply address; no picture or the PDF carries camera, location, or personal-name data. The database rules were tested from outside and hold. Redo this kind of check before any big publish.

---

## Style notes for new text on the site
Plain and dry, short headlines, no filler, few em dashes, no emoji. Use only facts he has given. When he says "placeholder", use plain Latin filler or a bracketed note, never something that looks real.
