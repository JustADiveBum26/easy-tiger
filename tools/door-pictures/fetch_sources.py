"""Downloads the free source pictures (about 25 MB) into source/. All are CC0 (free to use, no conditions).

  python tools/door-pictures/fetch_sources.py
"""
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source'); os.makedirs(SRC, exist_ok=True)
UA = {'User-Agent': 'EasyTigerProject/1.0 (private project; contact via GitHub JustADiveBum26)'}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()

# Poly Haven textures (CC0): the wood door and the iron plate
for asset, maps in (('wooden_gate', ('Diffuse', 'nor_gl', 'Rough')), ('metal_plate_02', ('Diffuse',))):
    files = json.loads(get(f'https://api.polyhaven.com/files/{asset}'))
    for m in maps:
        out = os.path.join(SRC, f'{asset}_{m}.jpg')
        open(out, 'wb').write(get(files[m]['2k']['jpg']['url'])); print('got', out)

# the tiger photo (CC0): "Tiger fangs (Unsplash).jpg" on Wikimedia Commons, by Jessica Weiller
url = 'https://upload.wikimedia.org/wikipedia/commons/c/cf/Tiger_fangs_%28Unsplash%29.jpg'
open(os.path.join(SRC, 'tiger_fangs.jpg'), 'wb').write(get(url)); print('got tiger_fangs.jpg')
