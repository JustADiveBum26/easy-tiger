# Easy Tiger Website: Handshake

Read this first. It's the main primer for everything in this folder. If something in here is out of date, tell Bradley and offer to fix it.

---

## What we're building

A small, private-feeling website for **Easy Tiger**, the speakeasy room Bradley is building in his basement in Columbia, Missouri. It's a fun, moody, 1920s Prohibition-style site that guests reach by link only. There's no domain name, no search listing, no public marketing. Just a link he hands to friends and family.

The name is a Mizzou Tigers nod. The room is a place to unplug after a long day: no phones, no screens, bottles meant to be opened and shared, not saved.

A visual mockup already exists (see "Mockup" below). This file holds the decisions so far so we don't redo them.

---

## Who you're working with

Bradley Jenkins. A few things about how he likes to work:

- **Casual tone, plain words.** No big words, no long winding sentences. Talk like a normal person.
- **Ask questions before big decisions.** Short, clear ones. Don't guess on anything that costs money, touches accounts, or is hard to undo.
- **Explain as you go.** He likes to learn why, not just get the result. One or two plain sentences is plenty.
- **He's comfortable with GitHub and Firebase.** He already has web apps on GitHub (his username is `justadivebum26`) and used Firebase for another project (a family shopping-list app). He is not a front-end developer, so keep the setup simple.
- **Anything written for the site should sound like a person wrote it.** Plain, warm, a little dry. Skip filler and buzzwords. Go easy on em dashes. Don't write like a brochure.

---

## Ground rules

1. **Ask before you:** push to GitHub, create or change any account or cloud setting, spend or commit money, or delete anything.
2. **Don't commit or push without his OK.** Keep commit messages short and plain.
3. **The repo is public.** GitHub Pages on a free account needs a public repo. So never put passwords, private keys, home address, phone numbers, or guests' personal info in any file in this folder.
4. **Small steps.** Build one piece, show it, get a thumbs up, move on.
5. **Keep it simple.** Plain HTML, CSS and JavaScript. No framework and no build step unless there's a real reason. If you think we need one, ask first.
6. **If something looks risky or wrong, say so,** even if he already asked for it.

---

## Decisions already made

- **Hosting:** GitHub Pages (free). Address will look like `justadivebum26.github.io/easy-tiger`. No domain to buy.
- **Privacy:** Link only. It's not locked down. Anyone with the link can open it. Add a `noindex` meta tag and a `robots.txt` that asks search engines to skip it. Be honest with him that this isn't real security.
- **Guest book and photo uploads:** Needs a small outside service, because GitHub Pages can only show pages, it can't save what guests type. Plan is **Firebase** (he's used it before). Guest book goes in Firestore.
- **Photos need approval first.** Nothing a guest uploads shows on the wall until Bradley approves it.
- **House password** on the guest book and photo upload, so a stranger who finds the link can't fill it with junk. This is a speed bump, not real security. See "Guest book and photos" for how to do it right.
- **Menu:** A PDF stored in the repo, linked from the site. Bradley will have Claude make the PDF version of the menu separately.
- **Look:** Dark, moody, classy, 1920s Prohibition. Details below.
- **Logo:** He has a finished logo (gold tiger head in an Art Deco circle, "EASY TIGER / COLUMBIA, MO"). Use it. Don't redraw or restyle it.
- **Site has one long page** with anchor links, not many separate pages. (Plus a hidden admin page for approving photos.)

## Still open (ask him, don't assume)

- **Where photos get stored:** Firebase Storage or Cloudinary. Firebase Storage may need a pay-as-you-go plan (with a spending cap, a small room's worth of photos would cost pennies). Cloudinary has a free tier. Lay out the trade-off in plain words and let him pick.
- **Do guest book entries need approval too,** or do they post right away? He only said photos need approval.
- **The tagline band.** The mockup shows "Speak softly · Pour generously · Stay late." Claude made that up as a placeholder. Confirm or replace it.
- **The "Knock to Enter" secret phrase.** Not chosen yet.
- **Story text.** The mockup has a short story based on what he's told us. He needs to add a few lines about how the idea started and who helped build it.
- **House password.** He picks it. Don't write it into a file in the repo.

---

## Sections on the page

In order, top to bottom:

1. **Nav bar.** Small logo, "Easy Tiger" in letterspaced caps, links to: Story, Build, Menu, Guest Book, Photos, Extras.
2. **Hero.** The logo big and centered, between burgundy velvet curtains with a gold rod across the top. Line under the logo: "Put the phone down. Stay a while." Two buttons: Come on in, See the menu.
3. **Gold band.** The tagline strip (placeholder, see above).
4. **The Story.** A few paragraphs plus an "In the room" box listing what's in the space.
5. **The Build.** Six construction photos with short captions, in build order (see "Assets").
6. **The Menu.** Button to open the PDF, plus the section names (House Drinks, Bourbon & Spirits, Wine, Pours We Remember). Next to it, a **Drink of the Night** card.
7. **Guest Book.** Name, note, house password, a Sign it button. Past entries listed next to the form.
8. **Photo Wall.** Add a photo button, a note that photos show up after approval, and a grid of approved photos in gold frames.
9. **The Extras.** Three cards: House Rules, Pours We Remember, Knock to Enter.
10. **Footer.** "Easy Tiger · Columbia, Missouri · Keep it between us."

### About the room (for the Story and "In the room" box)

Use only what's listed here. Don't invent details.

- Deep teal green walls (Sherwin-Williams Cascades) and a flat black ceiling with the pipes, ducts and joists painted black too
- One wall of **burned cedar** (shou sugi ban): torched, wire-brushed and oiled, so it's black charcoal with silver-grey grain, not honey colored
- Red leather sofa against the cedar wall, two brown Chesterfield chairs facing it, a hammered copper and bronze round coffee table, and a vintage-looking rug with two tigers on it
- Gold fixtures and warm amber Edison light only, no cool white light anywhere
- Exposed concrete floor, cleaned and sealed
- A burgundy velvet curtain where a door would be
- Prohibition-era art prints and gold animal busts on one wall, a record player on a dark walnut console

Don't put the street address anywhere on the site.

---

## Design

**Mood:** Dark, moody, classy 1920s speakeasy. Art Deco. Think gold foil on black, velvet, pinstripes, double-line frames.

**Colors** (these match the logo and the room):

| Use | Color |
|---|---|
| Gold (main accent, from the logo) | `#d4a846` |
| Page background, near black | `#070908` |
| Teal sections | `#0d1917` |
| Burgundy menu section | `#2a0d15` |
| Velvet curtain reds | `#3d0f1a`, `#5a1626`, `#2e0a13` |
| Main text, warm ivory | `#efe6d0` |
| Soft text | `#c9c0a8` and `#a8a08c` |

Keep the gold as one CSS variable so it's easy to swap.

**Fonts** (Google Fonts):
- **Playfair Display**, 600 weight, all caps with wide letter spacing, for headings
- **Cormorant Garamond** for body text and italic notes
- **Josefin Sans**, small caps with wide letter spacing, for labels and buttons

**Signature touches:**
- Gold **double-line frames** (a 1px border plus a 1px inner outline pulled in about 9px) on the menu card, guest book, extras and story box
- Photos sit in a thin gold frame with a dark mat
- Section headers: small gold label, big caps heading, then a thin gold line with a diamond in the middle
- Faint vertical **pinstripes** on the teal and burgundy sections
- **Burgundy velvet curtains** down both sides of the hero
- The logo has a pure black background, so on the page use `mix-blend-mode: screen` so it blends in with no box around it
- No emoji. Icons are simple thin gold line drawings.
- Must work on a phone. Most guests will open the link on their phone. Test small screens.

---

## Guest book and photos: how it should work

**Guest book:** Guest types name and note, enters the house password, taps Sign it. Entry saves to a Firestore collection (`guestbook`). The page reads and shows entries newest first.

**Photos:**
1. Guest picks a photo, enters the house password, taps upload.
2. The file goes into storage (Firebase Storage or Cloudinary, whichever he picks) and a record is saved in Firestore (`photos`) with `approved: false`.
3. The Photo Wall only shows records where `approved` is `true`.
4. Bradley has a hidden page, `admin.html`, not linked from the site. He signs in with his Google account (Firebase Auth). It shows waiting photos with **Approve** and **Delete** buttons.
5. Security rules only let his Google account change `approved` or delete anything.

**Be honest about the house password.** Anything checked only in the web page's JavaScript can be read by anyone who views the source. So:
- Do the check in the **Firebase security rules** too, not just on the page.
- Keep the real password **out of the repo**. It lives in the rules in the Firebase console, and Bradley tells guests the password in person.
- Also set simple limits in the rules: images only, a file size cap (around 8 MB), and a cap on the length of guest book notes.
- Explain this to him in plain words. Don't oversell it.

Put the Firebase config values in one small file (`js/firebase-config.js`). Those values aren't secret by themselves, since the security rules are what protect the data.

---

## The menu

- A PDF at `assets/menu/easy-tiger-menu.pdf`. To update the menu, replace that one file.
- The menu itself has sections for House Drinks, Bourbon & Spirits, Wine, and "Pours We Remember" (empty bottles, kept on the list because some were gifts or marked milestones).
- The PDF is made separately. Don't make up drinks or bottles for it.
- The look of the PDF should match the site: black, gold, Art Deco. The logo can go at the top.

---

## The fun extras

- **Drink of the Night.** Reads from `data/tonight.json` (drink name and one line). He edits that file by hand to change it. Later, a tiny form on the admin page could do it.
- **House Rules.** Phones stay out of the room. Open the bottle. Pour a little for the person next to you.
- **Pours We Remember.** A page or section for empty bottles, with who gave them and when. It starts empty. Needs a simple way to add entries.
- **Knock to Enter.** A fun gate at the front. Visitor types a secret phrase and the door "opens." Saves to the browser (`localStorage`) so they only do it once. This is for fun, not security. Say so.

Ideas he'd probably like, if we get time (ask first): a random Prohibition-era quote each visit, a "who's coming tonight" list, a record-of-the-week for the record player.

---

## Assets to put in this folder

Bradley saves these into `assets/`. Ask him for any that are missing.

- `assets/logo/easy-tiger-logo.png`: the gold tiger logo (black background)
- `assets/build/` : six construction photos, in the order they should show:
  1. Furring strips going up on the bare concrete wall
  2. Wiring and outlet boxes along the studs
  3. Framing the new wall
  4. Looking through the studs
  5. Drywall up and the burned cedar going on
  6. The finished burned cedar wall
- `assets/menu/easy-tiger-menu.pdf`: when it's ready

Shrink photos before putting them on the site (around 1600 px on the long side is plenty) so the page loads fast on a phone. Two of the build photos show the storage area behind the wall. Ask him if he wants those cropped.

---

## Suggested folder layout

```
/
├── CLAUDE.md            (this file)
├── index.html           (the whole front page)
├── admin.html           (hidden, for approving photos)
├── robots.txt
├── css/
│   └── style.css
├── js/
│   ├── main.js          (guest book, photo wall, knock gate)
│   ├── admin.js
│   └── firebase-config.js
├── data/
│   └── tonight.json
└── assets/
    ├── logo/
    ├── build/
    └── menu/
```

If you want to change this layout, tell him why first.

---

## Mockup

A visual mockup was made in Claude chat and is saved in Bradley's Claude artifacts as **"Easy Tiger Website Mockup."** It's the look he approved so far. If you can't open it, ask him for a screenshot and match the section list and design notes above. Everything marked [in brackets] in the mockup is a placeholder, not final text.

---

## Putting it on GitHub Pages (plain steps)

1. Make a new **public** repo called `easy-tiger` on his GitHub account.
2. Push these files to the `main` branch (after he says OK).
3. In the repo, go to Settings, then Pages, and set the source to the `main` branch, root folder.
4. After a minute or two the site is live at `justadivebum26.github.io/easy-tiger`.
5. Every push to `main` after that updates the site.

Tell him each step as you go, and check that it worked before the next one.

---

## First things to do in Claude Code

1. Read this file, then ask Bradley the open questions above. Keep it to a few at a time.
2. Check which assets are already in the folder and list what's missing.
3. Build the static page first: `index.html` and `css/style.css`, matching the design above, with placeholder text and photos. Show him on a phone-size view.
4. Add the `noindex` tag and `robots.txt`.
5. Get it live on GitHub Pages so he can open the link on his phone.
6. Then add the Firebase pieces: guest book first, then photo upload and approval, then the admin page.
7. Last, the fun extras.

---

## Notes to keep up to date

Add a line here each time a decision changes or a piece gets finished, so the next session picks up where this one left off.

- [x] Static page built (index.html, css/style.css, robots.txt, data/tonight.json, js/main.js stub). Uses Version 8 logo, black background, resized to 900px plus a 96px nav version. Tagline placeholder kept. Build photos and menu PDF still missing, so placeholder boxes show. Guest book and photo buttons are stubs until Firebase.
- [ ] Live on GitHub Pages
- [ ] Firebase project set up
- [ ] Guest book working
- [ ] Photo upload working
- [ ] Admin approval page working
- [x] Build photos added (Oct 8, 2026). Bradley gave 8 in "Easy Tiger Construction". Used 6, resized to 1600px wide JPGs in assets/build/ (originals stay in the Construction folder, never copy them into this folder, they're huge). Order: IMG_4633, 4729, 0263, 4733, 4839, 4832. Spares not used: IMG_4634 (another furring strips shot), IMG_4736 (close-up of an outlet box and ductwork). Photos 3 and 4 show the storage area behind the wall, not cropped yet, waiting on Bradley.
- [x] Guest book, photo upload, photo wall and admin page built as a DEMO (Oct 8, 2026). Everything saves through js/store.js (EasyStore), which is a demo version: it keeps data in the browser's localStorage only, so nothing is shared between people. Demo house password is "tiger" (shown on the page in demo mode; it is not the real one, which never goes in the repo). Demo admin "sign in" is just a button. main.js and admin.js only talk to EasyStore, so going real means writing a Firebase version of store.js with the same functions (listGuestbook, addGuestbook, deleteGuestbook, listPhotos({approved}), addPhoto, approvePhoto, deletePhoto, isAdmin, adminSignIn, adminSignOut) and nothing else should need to change. Photos are shrunk to 1400px JPEG in the browser before saving (also strips camera data). Limits match the plan: images only, 8 MB, name 60, note 400, caption 80. Guest book entries currently post right away (still an open question: should they need approval too?). admin.html is not linked from the site and has noindex. Tested end to end with a script: wrong password refused, entry shows newest first, typed HTML shows as plain text, photo stays off the wall until approved on admin.html. Still open: photo storage choice (Firebase Storage vs Cloudinary), the real house password, creating the Firebase project (needs Bradley's OK, touches his account). The "Firebase project set up" and the three items after it below are NOT done.
- [x] Drink of the Night removed for now (Oct 8, 2026, Bradley's call). The card, its code and data/tonight.json are gone. If it comes back, it's a small card plus a JSON file he edits by hand (see "The fun extras" above). The CSS/JS/HTML links carry ?v=3 so phones don't keep an old cached copy. Bump the number when changing those files.
- [x] Clickable menu (Oct 8, 2026). Source of truth is the menu Word file in "Easy Tiger Menus" (newest: Easy Tiger Spirits Menu10082026v2.docx; never use "Archived Menus"). Run `python tools/make-menu-data.py "<path to docx>"` (needs python-docx) to rebuild js/menu-data.js. It reads the docx by formatting (Heading 1 = type, bold 12 = drink name, italic 9.5 = maker/proof or "Built on", italic 9 = age/mash bill, regular 10 = notes). Then convert the docx to PDF (Word: File > Save As > PDF works, or Word COM from PowerShell) and replace assets/menu/easy-tiger-menu.pdf. Bump the ?v= number on the CSS/JS links in index.html so phones skip their cached copy. It is a .js file on purpose: browsers block fetch() of .json when a page is opened from a folder. Seven types now: Bourbon 51, Rye 13, Other American Whiskey 8, Tequila 1, Gin 3, Liqueur 7, House Drinks 27 (110 drinks). House Drinks have a "Built on ..." line (some have none) and a description, no proof/age. They are grouped by base spirit on the site (Bourbon, Rye, Other American Whiskey, Tequila, Gin, Vodka, same order as the menu types), worked out by tools/make-menu-data.py from the "Built on" bottle, or the first spirit in the description when there's no bottle or it's a liqueur. The script stops with a message if it can't tell a drink's base, so a new House Drink with an odd description may need a word added to BASE_WORDS. Within a group the drinks keep the Word file's order. UI: the menu card first shows only the list of types; clicking one opens its drinks in a fresh view with an "All types" back button; each drink opens to show notes. Bradley did NOT like the earlier tabs-plus-search version that showed the bourbon list right away, so do not bring it back. "Confirm on bottle" values are hidden on the site. Two tasting notes in the menu file still contain to-do wording (Redwood Empire Lost Monarch, Russell's Reserve 6 Year); Bradley fixes those in the Word file.
- [x] Menu PDF added (Oct 8, 2026) and replaced the same day with the v2 menu (now includes House Drinks), converted from the docx with Word. Lives at assets/menu/easy-tiger-menu.pdf. Wine and Pours We Remember are not in it yet. The cover still says "Spirits Menu".
- [ ] Extras added
