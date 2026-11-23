"""#46 Put that coffee down: three rows of two panels."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw, ImageFont
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/coffee"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK, CREAM = (20, 20, 20), (250, 246, 236)
HE = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"


def he_balloon(img, cx, cy, text, tail, size=28):
    """A balloon with one right-to-left Hebrew line, nikud shaped by raqm."""
    d = ImageDraw.Draw(img); f = ImageFont.truetype(HE, size)
    w = d.textlength(text, font=f, direction="rtl", language="he")
    bw, bh = w + 2 * size, size * 2.2
    base = [(cx - bw * .12, cy + bh / 2 - 4), (cx + bw * .06, cy + bh / 2 - 4)]
    d.polygon(base + [tail], fill=CREAM, outline=INK)
    d.rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), radius=bh / 2, fill=CREAM, outline=INK, width=2)
    d.polygon([(base[0][0] + 2, base[0][1] - 3), (base[1][0] - 2, base[1][1] - 3), (tail[0], tail[1] - 4)], fill=CREAM)
    d.text((cx, cy), text, font=f, fill=INK, anchor="mm", direction="rtl", language="he")


TEXT = {"c3.png": [(310, 30, ["Put that coffee down!"], (222, 108), 15, False, False)],
        "c4.png": [(440, 34, ["There was a moth", "in the relay."], (398, 205), 16, False, False)],
        "c5.png": [(640, 58, ["Put that coffee down!", "There was a fish", "in the percolator!"], (512, 128), 16, False, False)],
        "c6.png": [(440, 45, ["We know. Thanks!"], (312, 112), 18, False, False)]}
HEB = {}


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


page = Image.new("RGB", (W, 3 * H + 4 * G), "white"); d = ImageDraw.Draw(page)
for i in range(6):
    src = f"c{i + 1}.png"; im = fit(src, W2, H)
    for cx, cy, lines, tail, size, it, note in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, italic=it, note=note, size=size)
    if src in HEB:
        cx, cy, t, tail = HEB[src]; he_balloon(im, cx, cy, t, tail)
    x, y = G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)
    page.paste(im, (x, y)); d.rectangle((x, y, x + W2 - 1, y + H - 1), outline=INK, width=2)
page.save("s46.png"); print(page.size)
