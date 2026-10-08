"""
Turns the menu Word file into js/menu-data.js, which is what the site's clickable menu reads.

Run it from the Easy Tiger Webpage folder:
    python tools/make-menu-data.py "path/to/the-menu.docx"

It needs the python-docx package (pip install python-docx).

How it reads the Word file (so keep the menu in this shape):
  - Heading 1 .................. a type, like BOURBON or HOUSE DRINKS
  - Bold, 12 pt ................ a drink name
  - Italic, 9.5 pt ............. the maker line, "Maker, Place · 90 Proof"
                                 (for House Drinks: "Built on ...")
  - Italic, 9 pt ............... "Age: ... | Mash Bill: ..." (spirits only)
  - Regular, 10 pt ............. the tasting notes or description
"""
import io
import json
import os
import re
import sys

import docx

if len(sys.argv) != 2:
    sys.exit(__doc__)

src = sys.argv[1]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_path = os.path.join(root, 'js', 'menu-data.js')

doc = docx.Document(src)

categories = []
cat = None
cur = None


def size_of(p):
    r = p.runs[0] if p.runs else None
    return r.font.size.pt if r is not None and r.font.size else None


for p in doc.paragraphs:
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
        m = re.match(r'Age:\s*(.*?)\s*\|\s*Mash Bill:\s*(.*)$', text)
        if m:
            cur['age'], cur['details'] = m.group(1), m.group(2)
        else:
            m = re.match(r'Mash Bill:\s*(.*)$', text)
            cur['details'] = m.group(1) if m else text
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
