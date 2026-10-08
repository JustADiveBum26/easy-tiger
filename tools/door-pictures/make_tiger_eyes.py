"""KEPT FOR REFERENCE (opening v4): crops and re-lights the real tiger photo that sat behind the peephole.
Not used on the site now (the original glowing eyes are back), but the picture is still in assets/door/tiger-eyes.jpg.
Needs source/tiger_fangs.jpg (run fetch_sources.py first). Writes output/tiger-eyes.jpg."""
import os
import numpy as np
import cv2
from PIL import Image

HERE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE_DIR, 'source', 'tiger_fangs.jpg')
OUT = os.path.join(HERE_DIR, 'output'); os.makedirs(OUT, exist_ok=True)
rng = np.random.RandomState(11)

tig = np.asarray(Image.open(SRC).convert('RGB'), dtype=np.float32) / 255
cx, cy_eye = 2130, 1304                        # the middle of the face, and the height of the eyes, in the original photo
cw = 1480; ch = int(cw / 3.2)                  # a wide band, 3.2 times wider than tall, like the peephole
x0, y0 = cx - cw // 2, int(cy_eye - 0.52 * ch)
crop = cv2.resize(tig[y0:y0 + ch, x0:x0 + cw], (1280, 400), interpolation=cv2.INTER_AREA)
Hc, Wc = crop.shape[:2]
crop = np.clip((crop - 0.04) / 0.90, 0, 1) ** 1.45          # low-key: crush the shadows
crop *= np.array([1.12, 0.92, 0.70])                          # warm, like lantern light
yy, xx = np.mgrid[0:Hc, 0:Wc].astype(np.float32)
crop *= (np.clip(np.minimum(xx, Wc - xx) / (Wc * .26), 0, 1) ** 0.9 * np.clip(np.minimum(yy, Hc - yy) / (Hc * .30), 0, 1) ** 0.8)[..., None] * 1.35
for ex in (1872, 2388):                                       # warm glow in each eye
    ex_c, ey_c = (ex - x0) / cw * Wc, (1304 - y0) / ch * Hc
    crop += np.exp(-(((xx - ex_c) / 70) ** 2 + ((yy - ey_c) / 42) ** 2))[..., None] * np.array([0.40, 0.22, 0.04])
crop += rng.normal(0, 0.010, crop.shape).astype(np.float32)
x = np.arange(Wc, dtype=np.float32) / Wc                       # a little extra fade on the right edge (background rock)
crop *= np.where(x > 0.84, np.clip((1.0 - x) / 0.16, 0, 1) ** 1.2, 1.0)[None, :, None]
Image.fromarray((np.clip(crop, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, 'tiger-eyes.jpg'), quality=80, optimize=True)
print('wrote output/tiger-eyes.jpg')
