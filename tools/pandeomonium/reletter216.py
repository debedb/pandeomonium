"""hq#216: blank the lettering inside existing speech balloons and reletter them in Yiddish (RTL, nikud via raqm), Latin words in italic. Usage from Python: reletter(img, seed_xy, lines, size=34) where each line is a list of visual left-to-right segments (text, kind) with kind 'he', 'la' or 'la-i'."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HE = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
LA = "/System/Library/Fonts/Supplemental/Georgia{}.ttf"
INK = (20, 20, 20)
def _font(kind, size):
    if kind == "he": return ImageFont.truetype(HE, size)
    return ImageFont.truetype(LA.format(" Bold Italic" if kind == "la-i" else " Bold"), size)
def blank(img, seed):
    """Fill the balloon interior (light component around seed, plus the text holes it encloses) with its own median cream."""
    a = np.asarray(img.convert("RGB")).astype(int)
    light = (a.min(axis=2) > 195) & (a[..., 0] - a[..., 2] > 12) & (a[..., 0] - a[..., 2] < 50)  # warm cream, not grey sky
    # seed is approximate: take the largest light component reachable from points within 50px of it
    comp = np.zeros(light.shape, bool)
    for dy in range(-50, 51, 6):
        for dx in range(-50, 51, 6):
            x, y = seed[0] + dx, seed[1] + dy
            if not (0 <= y < light.shape[0] and 0 <= x < light.shape[1]) or not light[y, x] or comp[y, x]: continue
            bw = Image.fromarray((light * 255).astype(np.uint8)).copy()  # floodfill is a no-op on array-backed images
            ImageDraw.floodfill(bw, (x, y), 128)
            c = np.asarray(bw) == 128
            if comp.sum() < c.sum() < 120000: comp = c
    ys, xs = np.nonzero(comp)
    x0, y0, x1, y1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
    sub = Image.fromarray(np.where(comp[y0:y1, x0:x1], 255, 0).astype(np.uint8)).copy()
    ImageDraw.floodfill(sub, (0, 0), 64)
    inside = np.asarray(sub) != 64
    full = np.zeros(comp.shape, bool); full[y0:y1, x0:x1] = inside
    # shrink by 3px so the dark outline and its antialiasing stay intact
    m = Image.fromarray((full * 255).astype(np.uint8)).filter(__import__("PIL.ImageFilter", fromlist=["x"]).MinFilter(7))
    cream = tuple(int(v) for v in np.median(a[comp], axis=0))
    img.paste(Image.new("RGB", img.size, cream), (0, 0), m)
    return (x0, y0, x1, y1)
def reletter(img, seed, lines, size=34, center=None, lh=None):
    box = blank(img, seed)
    cx, cy = center or ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
    d = ImageDraw.Draw(img); lh = lh or int(size * 1.3)
    y = cy - lh * len(lines) / 2 + lh / 2
    for segs in lines:
        fonts = [_font(k, size) for _, k in segs]
        ws = [d.textlength(t, font=f, direction="rtl" if k == "he" else "ltr", language="yi" if k == "he" else None) for (t, k), f in zip(segs, fonts)]
        x = cx - sum(ws) / 2
        for (t, k), f, w in zip(segs, fonts, ws):
            if k == "he": d.text((x, y), t, font=f, fill=INK, anchor="lm", direction="rtl", language="yi")
            else: d.text((x, y), t, font=f, fill=INK, anchor="lm")
            x += w
        y += lh
