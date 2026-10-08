"""KEPT FOR REFERENCE (opening v3): the photo door with drawn brass hardware, plus the real tiger photo. Not used on the site now.
Builds the realistic door pictures for the password opening.
Sources (all free to use, no strings): Poly Haven CC0 textures (Wooden Gate, Metal Plate 02) and a CC0 tiger photo."""
import os
_HERE_DIR = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.join(_HERE_DIR, 'source')       # the downloaded pictures (run fetch_sources.py first)
OUT = os.path.join(_HERE_DIR, 'output')        # results go here; copy what you want into assets/door/
os.makedirs(OUT, exist_ok=True)
import os, json
import numpy as np
import cv2
from PIL import Image

os.chdir(HERE)
rng = np.random.RandomState(11)

W, H = 1000, 2174              # the door leaf, in pixels
S = 2                          # draw at 2x, then shrink: smooth edges
WW, HH = W * S, H * S

def load(path, size=None, gray=False):
    im = Image.open(path).convert('L' if gray else 'RGB')
    if size: im = im.resize(size, Image.LANCZOS)
    return np.asarray(im, dtype=np.float32) / 255.0

def blur(a, s): return cv2.GaussianBlur(a, (0, 0), s)

# ------------------------------------------------------------------ 1. the wood
tile = WW                                     # one texture tile is as wide as the door
diff = load('wooden_gate_Diffuse.jpg', (tile, tile))
nor = load('wooden_gate_nor_gl.jpg', (tile, tile))
rough = load('wooden_gate_Rough.jpg', (tile, tile), gray=True)
RAIL_Y = 367 * S                              # where the first cross-rail should land
# find the rail in the texture: the band with the least up/down grain, near the middle
rowvar = np.abs(np.diff(diff.mean(axis=2), axis=1)).mean(axis=1)
rail_in_tile = int(np.argmin(blur(rowvar.reshape(-1, 1), 6).ravel()[int(tile * .35):int(tile * .65)])) + int(tile * .35)
print('rail found at', round(rail_in_tile / tile, 3), 'of the tile')
shift = RAIL_Y - rail_in_tile
def tiled(a):
    reps = int(np.ceil(HH / tile)) + 2
    big = np.tile(a, (reps, 1, 1) if a.ndim == 3 else (reps, 1))
    start = (-shift) % tile + tile
    return big[start:start + HH]
leaf = tiled(diff)
N = tiled(nor) * 2 - 1                        # normal map: -1..1
R = tiled(rough[..., None])[..., 0]

# relight the planks from a lantern high and slightly left
L = np.array([-0.45, 0.50, 0.74]); L /= np.linalg.norm(L)       # x right, y up, z toward you
Nn = N / np.maximum(np.linalg.norm(N, axis=2, keepdims=True), 1e-6)
lam = np.clip(Nn @ L, 0, 1) / L[2]
Hv = (L + np.array([0, 0, 1])); Hv /= np.linalg.norm(Hv)
spec = np.clip(Nn @ Hv, 0, 1) ** 28 * (1 - R) * 0.55
leaf = leaf * (0.45 + 0.75 * lam[..., None]) + spec[..., None] * np.array([1.0, .82, .55])

# grade: warm, dark, heavy
leaf = leaf ** 1.18
leaf *= np.array([1.05, 0.93, 0.80])

# a pool of lantern light on the upper middle, fading to dark at the edges and the foot
yy, xx = np.mgrid[0:HH, 0:WW].astype(np.float32)
d2 = ((xx - WW * .5) / (WW * .62)) ** 2 + ((yy - HH * .30) / (HH * .36)) ** 2
pool = 0.30 + 0.95 * np.exp(-d2 * 1.4)
edge = np.clip(np.minimum(xx, WW - xx) / (WW * .14), 0, 1) ** 0.8
foot = 1 - 0.55 * np.clip((yy - HH * .72) / (HH * .28), 0, 1)
leaf *= (pool * (0.55 + 0.45 * edge) * foot)[..., None]
# grime: slow blotches, darker low down and around the edges
grime = blur(rng.rand(HH // 8, WW // 8).astype(np.float32), 6)
grime = cv2.resize(grime, (WW, HH), interpolation=cv2.INTER_CUBIC)
grime = 0.80 + 0.40 * (grime - grime.min()) / (np.ptp(grime) + 1e-6)
leaf *= grime[..., None]

# ------------------------------------------------------------------ 2. helpers for metal
LIGHT = np.array([-0.55, -0.62, 0.56]); LIGHT /= np.linalg.norm(LIGHT)   # image coords: x right, y DOWN, z toward you
HALF = LIGHT + np.array([0, 0, 1]); HALF /= np.linalg.norm(HALF)

def bevel_height(mask, bevel, scale=1.0):
    """mask float 0..1 -> a rounded-edge height map (so edges catch the light)"""
    m = (mask > 0.5).astype(np.uint8)
    dist = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    t = np.clip(dist / bevel, 0, 1)
    return bevel * scale * np.sqrt(1 - (1 - t) ** 2)

def shade(height, base, spec_k=0.7, shin=34, ambient=0.34, k=1.4, texture=None):
    gy, gx = np.gradient(blur(height, 1.0))
    n = np.dstack([-gx * k, -gy * k, np.ones_like(gx)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    lam = np.clip(n @ LIGHT, 0, 1)
    sp = np.clip(n @ HALF, 0, 1) ** shin * spec_k
    col = (texture if texture is not None else np.ones(height.shape + (3,), np.float32) * np.array(base, np.float32))
    return col * (ambient + (1 - ambient) * lam[..., None]) * 1.15 + sp[..., None] * np.array([1.0, .9, .65])

def put(canvas, y0, x0, rgb, alpha, shadow=(10, 14, 9, .62)):
    """paste a patch, with a soft shadow under it"""
    h, w = alpha.shape
    dx, dy, sb, sa = [v * S / 2 for v in shadow[:3]] + [shadow[3]]
    pad = int(sb * 4 + abs(dx) + abs(dy)) + 2
    Y0, X0 = max(0, y0 - pad), max(0, x0 - pad); Y1, X1 = min(HH, y0 + h + pad), min(WW, x0 + w + pad)
    sh = np.zeros((Y1 - Y0, X1 - X0), np.float32)
    ys, xs = y0 - Y0 + int(dy), x0 - X0 + int(dx)
    sh[ys:ys + h, xs:xs + w] = alpha
    sh = blur(sh, sb) * sa
    canvas[Y0:Y1, X0:X1] *= (1 - sh)[..., None]
    a = alpha[..., None]
    canvas[y0:y0 + h, x0:x0 + w] = canvas[y0:y0 + h, x0:x0 + w] * (1 - a) + rgb * a

def aa(mask_big):  # smooth edge from a hard 2x mask
    return np.clip(blur(mask_big.astype(np.float32), 0.9), 0, 1)

iron_t = load('metal_plate_02_Diffuse.jpg', (1400, 1400))
iron_t = (iron_t * np.array([0.78, 0.74, 0.70])) ** 1.15             # a bit darker and cooler
BRASS = (0.63, 0.46, 0.19)

# ------------------------------------------------------------------ 3. hinge straps along the two rails
for ry in (367, 1367):
    cy = int(ry * S); th = int(74 * S); length = int(660 * S); x0 = 0
    y0 = cy - th // 2
    m = np.zeros((th, length), np.uint8)
    pts = np.array([[0, 0], [length - int(th * .9), 0], [length, th // 2], [length - int(th * .9), th], [0, th]])
    cv2.fillPoly(m, [pts], 255)
    mask = aa(m)
    hgt = bevel_height(m, 7 * S, 1.0)
    # tile the iron picture over the strap, a different spot for each
    ox = rng.randint(0, 200); oy = rng.randint(0, 600)
    tex = cv2.resize(iron_t[oy:oy + 420, ox:ox + 1000], (length, th), interpolation=cv2.INTER_AREA)
    rgb = shade(hgt, None, spec_k=0.5, shin=22, ambient=0.30, k=1.2, texture=tex)
    put(leaf, y0, x0, rgb, mask, shadow=(8, 12, 8, .7))
    # rivets
    for rx in np.arange(60 * S, length - 120 * S, 92 * S):
        r = int(10 * S); size = 2 * r + 6
        yy2, xx2 = np.mgrid[0:size, 0:size].astype(np.float32); c = size / 2
        rr = np.hypot(yy2 - c, xx2 - c)
        mk = (rr <= r).astype(np.uint8) * 255
        hh = np.sqrt(np.clip(r * r - rr * rr, 0, None)) * 0.9
        rv = shade(hh, (0.20, 0.19, 0.18), spec_k=0.95, shin=40, ambient=0.28, k=0.5)
        put(leaf, cy - size // 2, int(rx), rv, aa(mk), shadow=(3, 5, 2.5, .55))

# ------------------------------------------------------------------ 4. the hatch frame (brass) around a dark recess
WIN_W, WIN_H, FR = 711, 222, 31
cx, cy = W // 2, 711
fx0, fy0 = (cx - WIN_W // 2 - FR) * S, (cy - WIN_H // 2 - FR) * S
fw, fh = (WIN_W + 2 * FR) * S, (WIN_H + 2 * FR) * S
m = np.zeros((fh, fw), np.uint8); cv2.rectangle(m, (0, 0), (fw - 1, fh - 1), 255, -1)
hole = np.zeros_like(m); cv2.rectangle(hole, (FR * S, FR * S), (fw - FR * S - 1, fh - FR * S - 1), 255, -1)
ring = cv2.subtract(m, hole)
hgt = bevel_height(ring, 9 * S, 1.0) + 0.02 * blur(rng.rand(fh, fw).astype(np.float32), 1) * S
rgb = shade(hgt, BRASS, spec_k=0.9, shin=30, ambient=0.30, k=1.5)
rgb *= (0.78 + 0.34 * blur(rng.rand(fh, fw).astype(np.float32), 4))[..., None]       # patina
rgb *= (0.94 + 0.10 * rng.rand(fh, 1, 1).astype(np.float32))                          # faint horizontal polish marks
put(leaf, fy0, fx0, rgb, aa(ring), shadow=(8, 12, 10, .8))
# the dark hole the shutter slides over
inner = np.zeros((WIN_H * S, WIN_W * S), np.float32)
leaf[(cy - WIN_H // 2) * S:(cy + WIN_H // 2) * S, (cx - WIN_W // 2) * S:(cx + WIN_W // 2) * S] = 0.02
# a few bolts on the frame corners
for bx, by in ((fx0 + 16 * S, fy0 + 16 * S), (fx0 + fw - 16 * S, fy0 + 16 * S), (fx0 + 16 * S, fy0 + fh - 16 * S), (fx0 + fw - 16 * S, fy0 + fh - 16 * S)):
    r = int(7 * S); size = 2 * r + 4
    yy2, xx2 = np.mgrid[0:size, 0:size].astype(np.float32); c = size / 2; rr = np.hypot(yy2 - c, xx2 - c)
    hh = np.sqrt(np.clip(r * r - rr * rr, 0, None)); bolt = shade(hh, BRASS, spec_k=1.0, shin=45, ambient=0.3, k=0.7)
    put(leaf, int(by - size / 2), int(bx - size / 2), bolt, aa(((rr <= r) * 255).astype(np.uint8)), shadow=(2, 3, 2, .5))

# ------------------------------------------------------------------ 5. keyhole plate on the right
kx, ky, kr = int(795 * S), int(1085 * S), int(52 * S)
size = 2 * kr + 8
yy2, xx2 = np.mgrid[0:size, 0:size].astype(np.float32); c = size / 2; rr = np.hypot(yy2 - c, xx2 - c)
disk = (rr <= kr).astype(np.uint8) * 255
kh = np.zeros_like(disk)
cv2.circle(kh, (int(c), int(c - 10 * S)), int(9 * S), 255, -1)
cv2.fillPoly(kh, [np.array([[c - 6 * S, c - 6 * S], [c + 6 * S, c - 6 * S], [c + 11 * S, c + 30 * S], [c - 11 * S, c + 30 * S]], np.int32)], 255)
plate = cv2.subtract(disk, kh)
hgt = bevel_height(plate, 7 * S, 1.0)
rgb = shade(hgt, BRASS, spec_k=1.0, shin=32, ambient=0.30, k=1.4)
rgb *= (0.90 + 0.18 * blur(rng.rand(size, size).astype(np.float32), 4))[..., None]
put(leaf, ky - size // 2, kx - size // 2, rgb, aa(plate), shadow=(5, 8, 6, .75))
# the dark keyhole itself, with a lip
leaf[ky - size // 2:ky - size // 2 + size, kx - size // 2:kx - size // 2 + size] *= (1 - 0.92 * aa(kh)[..., None])

# ------------------------------------------------------------------ 6. the ring knocker
ox, oy = W // 2 * S, int(1650 * S)
# backplate: a shield shape
bw, bh = int(150 * S), int(176 * S)
m = np.zeros((bh, bw), np.uint8)
pts = np.array([[bw * .5, 0], [bw, bh * .12], [bw * .93, bh * .60], [bw * .5, bh], [bw * .07, bh * .60], [0, bh * .12]], np.int32)
cv2.fillPoly(m, [pts], 255); m = cv2.GaussianBlur(m, (0, 0), 2 * S); m = (m > 127).astype(np.uint8) * 255
hgt = bevel_height(m, 14 * S, 1.0)
rgb = shade(hgt, BRASS, spec_k=0.95, shin=28, ambient=0.30, k=1.5)
rgb *= (0.90 + 0.18 * blur(rng.rand(bh, bw).astype(np.float32), 6))[..., None]
put(leaf, oy - int(bh * .72), ox - bw // 2, rgb, aa(m), shadow=(8, 14, 10, .85))
# the ring (a torus), hanging from a boss
R_out, R_in = int(66 * S), int(46 * S)
size = 2 * R_out + 10
yy2, xx2 = np.mgrid[0:size, 0:size].astype(np.float32); c = size / 2; rr = np.hypot(yy2 - c, xx2 - c)
mid = (R_out + R_in) / 2; half = (R_out - R_in) / 2
t = np.clip(1 - np.abs(rr - mid) / half, 0, 1)
ringmask = (np.abs(rr - mid) <= half).astype(np.uint8) * 255
hh = np.sqrt(np.clip(1 - (1 - t) ** 2, 0, 1)) * half * 1.1 * (ringmask > 0)
rgb = shade(hh, BRASS, spec_k=1.2, shin=36, ambient=0.28, k=1.1)
put(leaf, oy + int(bh * .28) - size // 2 + int(36 * S), ox - size // 2, rgb, aa(ringmask), shadow=(10, 16, 9, .9))
# the boss (a dome) where the ring hangs
r = int(20 * S); sz = 2 * r + 6
yy2, xx2 = np.mgrid[0:sz, 0:sz].astype(np.float32); cc = sz / 2; r2 = np.hypot(yy2 - cc, xx2 - cc)
hh = np.sqrt(np.clip(r * r - r2 * r2, 0, None))
put(leaf, oy + int(bh * .28) - int(60 * S), ox - sz // 2, shade(hh, BRASS, spec_k=1.1, shin=40, ambient=0.28, k=0.6), aa(((r2 <= r) * 255).astype(np.uint8)), shadow=(4, 7, 4, .7))

# ------------------------------------------------------------------ 7. a flickering lantern warmth over everything, then a little film grain
yy, xx = np.mgrid[0:HH, 0:WW].astype(np.float32)
warm = np.exp(-(((xx - WW * .5) / (WW * .55)) ** 2 + ((yy - HH * .28) / (HH * .30)) ** 2) * 1.6)
leaf *= (1 + 0.16 * warm[..., None] * np.array([1.0, 0.62, 0.20]))
leaf += rng.normal(0, 0.012, leaf.shape).astype(np.float32)
leaf = np.clip(leaf, 0, 1)

img = (cv2.resize(leaf, (W, H), interpolation=cv2.INTER_AREA) * 255).astype(np.uint8)
Image.fromarray(img).save(os.path.join(OUT, 'door-leaf.jpg'), quality=80, optimize=True, progressive=True)
print('door-leaf.jpg', img.shape, os.path.getsize(os.path.join(OUT, 'door-leaf.jpg')) // 1024, 'KB')

# window placement as fractions of the door (the page uses these for the tiger window)
geo = {'win_left': (cx - WIN_W / 2) / W, 'win_top': (cy - WIN_H / 2) / H, 'win_w': WIN_W / W, 'win_h': WIN_H / H, 'W': W, 'H': H}
json.dump(geo, open(os.path.join(HERE, 'geo.json'), 'w'), indent=1); print(geo)

# ------------------------------------------------------------------ 8. the shutter plate (worn iron, with a brass pull)
SW, SH = WIN_W + 6, WIN_H + 6
sx, sy = SW * S, SH * S
tex = cv2.resize(iron_t[300:300 + 360, 100:100 + 1100], (sx, sy), interpolation=cv2.INTER_AREA)
m = np.full((sy, sx), 255, np.uint8)
hgt = bevel_height(m, 12 * S, 1.0)
# two shallow grooves, and bolts
hgt[int(sy * .30):int(sy * .30) + 3 * S, :] -= 2 * S
hgt[int(sy * .70):int(sy * .70) + 3 * S, :] -= 2 * S
plate = shade(hgt, None, spec_k=0.65, shin=26, ambient=0.30, k=1.5, texture=tex) * 1.45
plate = np.clip(plate, 0, 1) ** 1.12
# four iron rivets
for rx, ry in ((46 * S, 40 * S), (sx - 46 * S, 40 * S), (46 * S, sy - 40 * S), (sx - 46 * S, sy - 40 * S)):
    r = int(11 * S); sz = 2 * r + 4
    yy3, xx3 = np.mgrid[0:sz, 0:sz].astype(np.float32); c3 = sz / 2; r3 = np.hypot(yy3 - c3, xx3 - c3)
    hh3 = np.sqrt(np.clip(r * r - r3 * r3, 0, None)); rv = shade(hh3, (0.22, 0.20, 0.19), spec_k=1.0, shin=40, ambient=0.28, k=0.6)
    a3 = aa(((r3 <= r) * 255).astype(np.uint8))[..., None]
    y3, x3 = int(ry - sz / 2), int(rx - sz / 2)
    plate[y3:y3 + sz, x3:x3 + sz] = plate[y3:y3 + sz, x3:x3 + sz] * (1 - a3) + rv * a3
# a brass pull at the bottom centre
pr = int(15 * S); pw = 2 * pr + 6
yy2, xx2 = np.mgrid[0:pw, 0:pw].astype(np.float32); pc = pw / 2; pr2 = np.hypot(yy2 - pc, xx2 - pc)
hh = np.sqrt(np.clip(pr * pr - pr2 * pr2, 0, None)); knob = shade(hh, BRASS, spec_k=1.1, shin=42, ambient=0.3, k=0.7)
pa = aa(((pr2 <= pr) * 255).astype(np.uint8))[..., None]
y0k, x0k = sy - int(34 * S) - pw // 2, sx // 2 - pw // 2
plate[y0k:y0k + pw, x0k:x0k + pw] = plate[y0k:y0k + pw, x0k:x0k + pw] * (1 - pa) + knob * pa
plate *= 0.78
sh_img = (np.clip(cv2.resize(plate, (SW, SH), interpolation=cv2.INTER_AREA), 0, 1) * 255).astype(np.uint8)
Image.fromarray(sh_img).save(os.path.join(OUT, 'shutter.jpg'), quality=82, optimize=True)
print('shutter.jpg', sh_img.shape, os.path.getsize(os.path.join(OUT, 'shutter.jpg')) // 1024, 'KB')

# ------------------------------------------------------------------ 9. the frame around the door: a plain dark wood tile
jt = load('wooden_gate_Diffuse.jpg', (700, 700))
jt = (jt ** 1.3) * np.array([0.55, 0.45, 0.36])
Image.fromarray((np.clip(jt, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, 'jamb.jpg'), quality=72, optimize=True)
print('jamb.jpg', os.path.getsize(os.path.join(OUT, 'jamb.jpg')) // 1024, 'KB')

# ------------------------------------------------------------------ 10. the tiger behind the hatch (a real photo, relit like it is lit by a lantern)
tig = np.asarray(Image.open('tiger_fangs.jpg').convert('RGB'), dtype=np.float32) / 255
x0, x1, y0, y1 = 1290, 2970, 1030, 1555             # a wide band: brow stripes, both eyes, the cheeks
crop = tig[y0:y1, x0:x1]
crop = cv2.resize(crop, (1280, 400), interpolation=cv2.INTER_AREA)
Hc, Wc = crop.shape[:2]
# low-key: crush the shadows, warm the whole thing, keep the stripes crisp
crop = np.clip((crop - 0.04) / 0.90, 0, 1) ** 1.45
crop *= np.array([1.12, 0.92, 0.70])
yy, xx = np.mgrid[0:Hc, 0:Wc].astype(np.float32)
vx = np.clip(np.minimum(xx, Wc - xx) / (Wc * .30), 0, 1) ** 0.9              # fade to black at the left and right
vy = np.clip(np.minimum(yy, Hc - yy) / (Hc * .30), 0, 1) ** 0.8              # and top and bottom
crop *= (vx * vy)[..., None] * 1.35
# cast a warm glow into the eyes
eyes = ((1872 - x0) / (x1 - x0) * Wc, (1304 - y0) / (y1 - y0) * Hc), ((2388 - x0) / (x1 - x0) * Wc, (1304 - y0) / (y1 - y0) * Hc)
for ex, ey in eyes:
    g = np.exp(-(((xx - ex) / 70) ** 2 + ((yy - ey) / 42) ** 2))
    crop += g[..., None] * np.array([0.40, 0.22, 0.04])
crop += rng.normal(0, 0.010, crop.shape).astype(np.float32)
Image.fromarray((np.clip(crop, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, 'tiger-eyes.jpg'), quality=80, optimize=True)
eye_pct = [(round(ex / Wc * 100, 1), round(ey / Hc * 100, 1)) for ex, ey in eyes]
print('tiger-eyes.jpg', os.path.getsize(os.path.join(OUT, 'tiger-eyes.jpg')) // 1024, 'KB', '| eye positions (% of width, % of height):', eye_pct)
json.dump({'eyes_pct': eye_pct}, open(os.path.join(HERE, 'eyes.json'), 'w'))
