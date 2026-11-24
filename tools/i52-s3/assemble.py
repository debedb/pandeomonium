"""#52 The Cranes strip 3: three rows of two panels."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/cranes/s3"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK = (20, 20, 20)
TEXT = {"c1.png": [(190, 58, ["Wasn't there another one?"], (282, 150), 15)],
        "c2.png": [(500, 40, ["A crane?"], (432, 210), 16), (200, 100, ["That's what they said."], (292, 165), 15)],
        "c3.png": [(200, 40, ["Так что тс-с..."], (385, 72), 13), (565, 42, ["Тс-с..."], (452, 76), 13)],
        "c4.png": [(640, 40, ["There is clearly", "a connection."], (628, 190), 15), (300, 120, ["Between what?"], (410, 112), 15)],
        "c5.png": [(430, 28, ["...before we move on to the second class,", "there's the question of envelopes..."], (300, 98), 13)],
        "c6.png": [(230, 35, ["Humans."], (215, 86), 17)]}


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


page = Image.new("RGB", (W, 3 * H + 4 * G), "white"); d = ImageDraw.Draw(page)
for i in range(6):
    src = f"c{i + 1}.png"; im = fit(src, W2, H)
    for cx, cy, lines, tail, size in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, size=size)
    x, y = G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)
    page.paste(im, (x, y)); d.rectangle((x, y, x + W2 - 1, y + H - 1), outline=INK, width=2)
page.save("s52-3.png"); print(page.size)
