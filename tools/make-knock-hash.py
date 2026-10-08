"""
Turns the Knock to Enter words into the scrambled fingerprint the site checks.

    python tools/make-knock-hash.py "the secret words"

Paste the long code it prints into js/firebase-config.js, between the quotes after hash:
Capital letters, spaces and punctuation don't matter, so "Open Sesame!" and "open sesame" are the same.
Changing the words changes the code, which also makes everyone who already knocked knock again.
"""
import hashlib
import re
import sys
import unicodedata

if len(sys.argv) != 2 or not sys.argv[1].strip():
    sys.exit(__doc__)

plain = unicodedata.normalize('NFD', sys.argv[1].lower())
plain = ''.join(ch for ch in plain if not unicodedata.combining(ch))
plain = re.sub(r'[^a-z0-9]+', '', plain)
if not plain:
    sys.exit('The words need at least one letter or number.')
print(hashlib.sha256(('easy-tiger:' + plain).encode('utf-8')).hexdigest())
