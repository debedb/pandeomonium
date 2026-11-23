"""#19 Data, Lore, and Mandela: two rows of three square panels, then a wide final panel; the PADD transcript is lettered onto the screen."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw, ImageFont
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/mandela"))
G, W = 6, 1536
W3 = (W - 4 * G) // 3; HW = 900; W1 = W - 2 * G
INK = (20, 20, 20)
MONO = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
TEXT = {"c1.png": [(330, 48, ["Sam, she's not coming", "through that door."], (290, 118), 15)],
        "c2.png": [(130, 40, ["Correction."], (95, 100), 16)],
        "c3.png": [(300, 42, ["Nobody remembers", "it that way."], (282, 120), 16)],
        "c7.png": [(905, 110, ["Play it again, Sam."], (915, 222), 22)]}
PADD = (264, 262, 442, 386)  # c2 screen, panel coords


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


def padd(im):
    d = ImageDraw.Draw(im); f = ImageFont.truetype(MONO, 15)
    x0, y0, x1, y1 = PADD; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.text((cx, cy), "“She would not be\ncoming back here.”", font=f, fill=(70, 40, 10), anchor="mm", align="center", spacing=6)


page = Image.new("RGB", (W, 2 * W3 + HW + 4 * G), "white"); d = ImageDraw.Draw(page)
for i in range(7):
    src = f"c{i + 1}.png"
    w, h = (W3, W3) if i < 6 else (W1, HW)
    im = fit(src, w, h, ty=float(os.environ.get("TY7", "0.75")) if i == 6 else 0.5)
    if src == "c2.png": padd(im)
    for cx, cy, lines, tail, size in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, size=size)
    x, y = (G + (i % 3) * (W3 + G), G + (i // 3) * (W3 + G)) if i < 6 else (G, G + 2 * (W3 + G))
    page.paste(im, (x, y)); d.rectangle((x, y, x + w - 1, y + h - 1), outline=INK, width=2)
page.save("s19.png"); print(page.size)
