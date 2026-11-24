"""#48 strip 1 The Appointment: three square panels, two wide panels, then a full-width final panel; the lead card is lettered onto the card."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw, ImageFont
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/orchard"))
G, W = 6, 1536
W3 = (W - 4 * G) // 3; W2 = (W - 3 * G) // 2; H2 = round(W2 * 1024 / 1536); W1 = W - 2 * G; H6 = 640
INK = (20, 20, 20)
TYPE = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
TEXT = {"c1.png": [(150, 40, ["Mrs. Ranevskaya?"], (215, 120), 16)],
        "c2.png": [(300, 40, ["Shelley Levene.", "I have something I'd", "like you to look at."], (282, 104), 15)],
        "c3.png": [(170, 34, ["Lyubov Andreyevna.", "The auction is on", "the twenty-second."], (362, 104), 14)],
        "c4.png": [(250, 50, ["Lease the plots for summer houses.", "Twenty-five thousand a year.", "The land stays yours."], (330, 150), 15)],
        "c5.png": [(560, 50, ["It hasn't changed at all."], (520, 140), 16)]}
CARD = (320, 307, 382, 4)  # (x0, y0, x1, y1, angle) on c1 once the card is located


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


def card(im):
    x0, y0, x1, ang = CARD
    t = Image.new("RGBA", (400, 80), (0, 0, 0, 0)); ImageDraw.Draw(t).text((200, 40), "L. RANEVSKAYA", font=ImageFont.truetype(TYPE, 44), fill=(40, 40, 60), anchor="mm")
    t = t.resize((x1 - x0, round((x1 - x0) * 80 / 400)), Image.LANCZOS).rotate(ang, expand=True, resample=Image.BICUBIC)
    im.paste(t, (x0, y0), t)


boxes = [(W3, W3)] * 3 + [(W2, H2)] * 2 + [(W1, H6)]
pos = [(G + i * (W3 + G), G) for i in range(3)] + [(G + i * (W2 + G), 2 * G + W3) for i in range(2)] + [(G, 3 * G + W3 + H2)]
page = Image.new("RGB", (W, 4 * G + W3 + H2 + H6), "white"); d = ImageDraw.Draw(page)
for i, ((w, h), (x, y)) in enumerate(zip(boxes, pos)):
    src = f"c{i + 1}.png"; im = fit(src, w, h, ty=float(os.environ.get("TY6", "0.5")) if i == 5 else 0.5)
    if src == "c1.png" and CARD: card(im)
    for cx, cy, lines, tail, size in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, size=size)
    page.paste(im, (x, y)); d.rectangle((x, y, x + w - 1, y + h - 1), outline=INK, width=2)
page.save("s48-1.png"); print(page.size)
