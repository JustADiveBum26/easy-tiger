"""
Turns the menu Word file into js/menu-data.js, which is what the site's clickable menu reads.

Run it from the Easy Tiger Webpage folder:
    python tools/make-menu-data.py "path/to/the-menu.docx" [--inventory "path/to/inventory.json"]

  With --inventory, each house drink also gets its glass (a "glass" name and a "glassImg" picture name) so the site can show a
  small picture of the glass. The weekly update passes it automatically.

It needs the python-docx package (pip install python-docx).

How it reads the Word file (so keep the menu in this shape):
  - Heading 1 .................. a type, like BOURBON or HOUSE DRINKS
  - Bold, 12 pt ................ a drink name
  - Italic, 9.5 pt ............. the maker line, "Maker, Place · 90 Proof"
                                 (for House Drinks: "Built on ...")
  - Italic, 9 pt ............... "Age: ... | Mash Bill: ... | extra note" (spirits only; any part can be missing)
  - Regular, 10 pt ............. the tasting notes or description
"""
import io
import json
import os
import re
import sys

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

args = sys.argv[1:]
inventory_path = None
if '--inventory' in args:                      # optional: the menu data file, used to add each house drink's glass
    i = args.index('--inventory')
    inventory_path = args[i + 1] if i + 1 < len(args) else None
    del args[i:i + 2]
if len(args) != 1 or (('--inventory' in sys.argv) and not inventory_path):
    sys.exit(__doc__)

src = args[0]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_path = os.path.join(root, 'js', 'menu-data.js')

doc = docx.Document(src)

categories = []
cat = None
cur = None


def size_of(p):
    r = p.runs[0] if p.runs else None
    return r.font.size.pt if r is not None and r.font.size else None


def all_paragraphs(document):
    """Paragraphs in page order, including the ones inside tables (a house drink with a glass picture sits in a table row)."""
    for child in document.element.body.iterchildren():
        if child.tag.endswith('}p'):
            yield Paragraph(child, document)
        elif child.tag.endswith('}tbl'):
            done = set()
            for row in Table(child, document).rows:
                for cell in row.cells:
                    if id(cell._tc) in done:
                        continue
                    done.add(id(cell._tc))
                    for p in cell.paragraphs:
                        yield p


for p in all_paragraphs(doc):
    text = re.sub(r'\s+', ' ', p.text).strip()
    if not text or not p.runs:
        continue
    r = p.runs[0]
    size = size_of(p)

    if p.style.name == 'Heading 1':
        cat = {'name': text.title(), 'drinks': []}
        cat['id'] = re.sub(r'[^a-z]+', '-', cat['name'].lower()).strip('-')
        categories.append(cat)
        cur = None
    elif cat is None:
        continue  # cover page
    elif r.bold and size == 12:
        cur = {'name': text, 'maker': '', 'proof': '', 'age': '', 'details': '', 'notes': ''}
        cat['drinks'].append(cur)
    elif cur is None:
        continue
    elif r.italic and size == 9.5:
        cur['maker'] = text
    elif r.italic and size == 9:
        # "Age: 11 Years   |   Mash Bill: ...   |   Warehouse B, 212 barrels". Any part can be missing,
        # and a part with no label (like the warehouse) is kept as the bottle's extra note.
        known = False
        for part in [x.strip() for x in text.split('|') if x.strip()]:
            if part.startswith('Age:'):
                cur['age'], known = part[4:].strip(), True
            elif part.startswith('Mash Bill:'):
                cur['details'], known = part[10:].strip(), True
            elif known:
                cur['provenance'] = (cur.get('provenance', '') + ' · ' + part).strip(' ·')
        if not known:
            cur['details'] = text
    elif size == 10:
        cur['notes'] = (cur['notes'] + ' ' + text).strip()

# "Maker, Place · 125 Proof" -> maker + proof
for c in categories:
    for d in c['drinks']:
        if ' · ' in d['maker']:
            maker, proof = d['maker'].rsplit(' · ', 1)
            d['maker'], d['proof'] = maker.strip(), proof.strip()

# House Drinks are grouped by base spirit, in the same order as the menu's types.
# The base comes from the "Built on ..." bottle when that bottle is on the menu
# (so Gentleman Jack makes a Whiskey Ginger a Tennessee whiskey drink), and from the
# first spirit named in the description otherwise (Cointreau, Chambord, no bottle at all).
BASE_ORDER = ['Bourbon', 'Rye', 'Other American Whiskey', 'Tequila', 'Gin', 'Vodka']
BASE_WORDS = [('bourbon', 'Bourbon'), ('rye', 'Rye'), ('tequila', 'Tequila'), ('gin', 'Gin'), ('vodka', 'Vodka'),
              ('whiskey', 'Other American Whiskey')]
BOTTLE_TYPES = {'bourbon': 'Bourbon', 'rye': 'Rye', 'other-american-whiskey': 'Other American Whiskey',
                'tequila': 'Tequila', 'gin': 'Gin'}

bottles = []  # (lowercase bottle name, base) for every non-liqueur spirit on the menu
for c in categories:
    if c['id'] in BOTTLE_TYPES:
        for d in c['drinks']:
            bottles.append((d['name'].lower(), BOTTLE_TYPES[c['id']]))
bottles.sort(key=lambda b: -len(b[0]))  # longest name first, so "Seagram's Extra Dry Gin" beats a shorter match


def base_of(drink):
    built_on = re.sub(r'^built on\s*', '', drink['maker'], flags=re.I).lower()
    for name, base in bottles:
        if name in built_on:
            return base
    words = re.findall(r'[a-z]+', drink['notes'].lower())
    for word, base in BASE_WORDS:
        if word in words:
            return base
    return None


for c in categories:
    if c['id'] != 'house-drinks':
        continue
    for d in c['drinks']:
        d['base'] = base_of(d)
    unknown = [d['name'] for d in c['drinks'] if d['base'] not in BASE_ORDER]
    if unknown:
        sys.exit('Could not tell the base spirit for: ' + ', '.join(unknown))
    # stable sort: grouped by base, still in the Word file's order inside each group
    c['drinks'].sort(key=lambda d: BASE_ORDER.index(d['base']))

# Glass for each house drink (the picture file name comes from glass_art/glass_types.json next to the inventory file).
# The drinks sheet owns this; the Word menu only carries the pictures, so it is read from the inventory by drink name.
if inventory_path:
    inv = json.load(io.open(inventory_path, encoding='utf-8'))
    glass_by_drink = {d['name'].strip().lower(): d.get('glass', '') for d in inv.get('drinks', [])}
    types_path = os.path.join(os.path.dirname(os.path.abspath(inventory_path)), 'glass_art', 'glass_types.json')
    img_of = {t['name']: t['file'] for t in json.load(io.open(types_path, encoding='utf-8'))} if os.path.exists(types_path) else {}
    for c in categories:
        if c['id'] != 'house-drinks':
            continue
        for d in c['drinks']:
            g = glass_by_drink.get(d['name'].strip().lower(), '')
            if g and g in img_of:
                d['glass'], d['glassImg'] = g, img_of[g]

with io.open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write('// Made from the menu Word file by tools/make-menu-data.py. Re-run it after the menu changes.\n')
    f.write('// It is a script (not .json) so the page also works when opened straight from a folder.\n')
    f.write('const MENU = ')
    json.dump({'title': 'Menu', 'categories': categories}, f, ensure_ascii=False, indent=2)
    f.write(';\n')

total = 0
for c in categories:
    print('%-24s %3d' % (c['name'], len(c['drinks'])))
    total += len(c['drinks'])
    for d in c['drinks']:
        missing = [k for k in ('name', 'notes') if not d[k]]
        if missing:
            print('  CHECK:', d['name'], 'is missing', missing)
print('%-24s %3d' % ('TOTAL', total))
