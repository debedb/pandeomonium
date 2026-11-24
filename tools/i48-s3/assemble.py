"""#48 strip 3 Closing Time: two panels, the wide house-into-library panel, two panels, then the wide kick; SFX lettered by hand."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw, ImageFont
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/orchard/s3"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536); W1 = W - 2 * G; H3, H6 = 600, 660
INK = (20, 20, 20)
SFXF = "/System/Library/Fonts/Supplemental/Impact.ttf"
TEXT = {"c4.png": [(430, 34, ["You see..."], (332, 100), 15),
                   (480, 120, ["You don't", "understand", "anything."], (336, 136), 15),
                   (470, 250, ["So you see..."], (330, 168), 15)],
        "c5.png": [(130, 330, ["Observe closely,", "Grace Hopper."], (200, 215), 16)]}
SFX = {"c1.png": (650, 300, "CLICK", 30, 0), "c6.png": (1060, 50, "THWACK", 64, 8)}
TY = {"c3.png": 0.3, "c6.png": 0.2}


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


def sfx(im, x, y, text, size, ang):
    f = ImageFont.truetype(SFXF, size); d0 = ImageDraw.Draw(im)
    bw = int(d0.textlength(text, font=f)) + size; t = Image.new("RGBA", (bw, int(size * 1.6)), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((bw // 2, int(size * .8)), text, font=f, fill=(250, 240, 200), anchor="mm", stroke_width=max(2, size // 12), stroke_fill=INK)
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC); im.paste(t, (x - t.width // 2, y - t.height // 2), t)


ORDER = ["c1.png", "c2.png", "c3.png", "c4.png", "c5.png", "c6.png"]
boxes = [(W2, H), (W2, H), (W1, H3), (W2, H), (W2, H), (W1, H6)]
y2 = G + H + G; y3 = y2 + H3 + G; y4 = y3 + H + G
pos = [(G, G), (2 * G + W2, G), (G, y2), (G, y3), (2 * G + W2, y3), (G, y4)]
page = Image.new("RGB", (W, y4 + H6 + G), "white"); d = ImageDraw.Draw(page)
for src, (w, h), (x, y) in zip(ORDER, boxes, pos):
    im = fit(src, w, h, ty=TY.get(src, 0.5))
    if src in SFX: sfx(im, *SFX[src])
    for cx, cy, lines, tail, size in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, size=size)
    page.paste(im, (x, y)); d.rectangle((x, y, x + w - 1, y + h - 1), outline=INK, width=2)
page.save("s48-3.png"); print(page.size)
