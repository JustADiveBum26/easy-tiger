"""IN USE (opening v7): cuts the engraved gold tiger out of the logo and lights it like a gold-leaf print in lantern light.
It writes tiger-engraved.jpg (1400 x 437, the shape of the peephole) into output/.

  python tools/door-pictures/make_engraved_tiger.py "path/to/02_Easy_Tiger_HERO_Black_Background_5000px.png"

The logo file is the 5000 px Version 8 hero picture (it lives in the Easy Tiger Logo folder, not in this project)."""
import os
import sys
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
if len(sys.argv) != 2:
    sys.exit(__doc__)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output'); os.makedirs(OUT, exist_ok=True)

logo = Image.open(sys.argv[1]).convert('RGB')
EY, LX, RX = 1820, 2052, 2892                     # where the eyes are in the 5000 px logo
cw = 2500; ch = int(cw / 3.2)                      # a band 3.2 times wider than tall, the shape of the peephole
x0 = (LX + RX) // 2 - cw // 2; y0 = int(EY - 0.50 * ch)
band = np.asarray(logo.crop((x0, y0, x0 + cw, y0 + ch)).resize((1400, 437), Image.LANCZOS), dtype=np.float32) / 255
H, W = band.shape[:2]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
band = (band ** 1.7) * 0.82 * np.array([1.10, 0.84, 0.52])                  # deeper and warmer: lantern-lit gold
band *= ((np.clip(np.minimum(xx, W - xx) / (W * .30), 0, 1)) * (np.clip(np.minimum(yy, H - yy) / (H * .34), 0, 1) ** 0.9))[..., None]   # melt into the dark
for ex in ((LX - x0) / cw * W, (RX - x0) / cw * W):                           # the eyes catch the light
    ey = (EY - y0) / ch * H
    band += np.exp(-(((xx - ex) / 60) ** 2 + ((yy - ey) / 38) ** 2))[..., None] * np.array([0.34, 0.19, 0.03])
Image.fromarray((np.clip(band, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, 'tiger-engraved.jpg'), quality=88)
print('wrote output/tiger-engraved.jpg; the eyes sit at %.1f%% and %.1f%% across, halfway down' % ((LX - x0) / cw * 100, (RX - x0) / cw * 100))
