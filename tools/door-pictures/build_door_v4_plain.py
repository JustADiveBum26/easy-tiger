"""IN USE (opening v4, current): the seamless plank tile (door-wood.jpg) and the plain wooden slider (shutter.jpg).
Door pictures, version 2: no hardware. A seamless, re-lit plank tile that fills any screen, plus a plain wooden shutter."""
import os
_HERE_DIR = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.join(_HERE_DIR, 'source')       # the downloaded pictures (run fetch_sources.py first)
OUT = os.path.join(_HERE_DIR, 'output')        # results go here; copy what you want into assets/door/
os.makedirs(OUT, exist_ok=True)
import os
import numpy as np
import cv2
from PIL import Image

os.chdir(HERE)

T = 1400                                   # tile size in pixels
def load(path, size, gray=False):
    im = Image.open(path).convert('L' if gray else 'RGB').resize(size, Image.LANCZOS)
    return np.asarray(im, dtype=np.float32) / 255.0

diff = load('wooden_gate_Diffuse.jpg', (T, T))
nor = load('wooden_gate_nor_gl.jpg', (T, T)) * 2 - 1
rough = load('wooden_gate_Rough.jpg', (T, T), gray=True)

# relight the planks from a lantern high and a little to the left (this is per-pixel, so the tile still repeats seamlessly)
L = np.array([-0.45, 0.50, 0.74]); L /= np.linalg.norm(L)
Nn = nor / np.maximum(np.linalg.norm(nor, axis=2, keepdims=True), 1e-6)
lam = np.clip(Nn @ L, 0, 1) / L[2]
Hv = L + np.array([0, 0, 1]); Hv /= np.linalg.norm(Hv)
spec = np.clip(Nn @ Hv, 0, 1) ** 28 * (1 - rough) * 0.5
wood = diff * (0.45 + 0.75 * lam[..., None]) + spec[..., None] * np.array([1.0, .82, .55])
wood = np.clip(wood, 0, 1) ** 1.12 * np.array([1.06, 0.94, 0.82]) * 1.05      # warm, a bit darker
wood = np.clip(wood, 0, 1)
Image.fromarray((wood * 255).astype(np.uint8)).save(os.path.join(OUT, 'door-wood.jpg'), quality=80, optimize=True, progressive=True)
print('door-wood.jpg', os.path.getsize(os.path.join(OUT, 'door-wood.jpg')) // 1024, 'KB')

# where the cross-rail sits inside the tile, as a fraction (the page uses it to place the rail neatly)
rowvar = np.abs(np.diff(diff.mean(axis=2), axis=1)).mean(axis=1)
sm = cv2.GaussianBlur(rowvar.reshape(-1, 1), (0, 0), 6).ravel()
lo, hi = int(T * .35), int(T * .65)
print('rail at', round((int(np.argmin(sm[lo:hi])) + lo) / T, 3), 'of the tile')

# the shutter: a plain wooden slider, a little darker, with edges that catch the light
SW, SH = 717, 228
rng = np.random.RandomState(5)
CW, CH = int(SW * 1.6), int(SH * 1.6)
ox, oy = rng.randint(0, T - CW), rng.randint(0, T - CH)
crop = wood[oy:oy + CH, ox:ox + CW]
crop = cv2.resize(crop, (SW, SH), interpolation=cv2.INTER_AREA) * 0.72
yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
edge = np.minimum(np.minimum(xx, SW - 1 - xx), np.minimum(yy, SH - 1 - yy))
crop *= (0.55 + 0.45 * np.clip(edge / 18, 0, 1) ** 0.8)[..., None]                         # darker toward the edges
crop[:3] += np.array([0.10, 0.07, 0.04]) * np.clip(1 - np.arange(3) / 3, 0, 1)[:, None, None]  # a thin lit top edge
crop += rng.normal(0, 0.008, crop.shape).astype(np.float32)
Image.fromarray((np.clip(crop, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, 'shutter.jpg'), quality=82, optimize=True)
print('shutter.jpg', os.path.getsize(os.path.join(OUT, 'shutter.jpg')) // 1024, 'KB')

