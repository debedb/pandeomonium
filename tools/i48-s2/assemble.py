"""#48 strip 2 The Transaction: three rows of two panels, then a square panel 7 and a wide, still panel 8."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/orchard/s2"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536); W3 = (W - 4 * G) // 3; W8 = W - 3 * G - W3
INK = (20, 20, 20)
TEXT = {"c1.png": [(330, 32, ["Who bought it?"], (388, 182), 16), (110, 255, ["I bought it."], (160, 142), 16)],
        "c4.png": [(390, 40, ["Where will you go?"], (278, 112), 16)],
        "c5.png": [(420, 34, ["The Ragulins. They've asked me", "to run the household."], (502, 92), 15),
                   (360, 180, ["I'm taking the", "Kharkov train."], (262, 140), 15)],
        "c6.png": [(200, 150, ["There was snow", "this time last year."], (192, 228), 13),
                   (590, 190, ["Our thermometer's", "broken."], (590, 252), 13)],
        "c7.png": [(372, 78, ["Yermolai Alexeyevich!"], (430, 0), 15), (55, 220, ["Coming."], (70, 158), 15)]}


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


boxes = [(W2, H)] * 6 + [(W3, W3), (W8, W3)]
pos = [(G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)) for i in range(6)]
y4 = G + 3 * (H + G); pos += [(G, y4), (2 * G + W3, y4)]
page = Image.new("RGB", (W, y4 + W3 + G), "white"); d = ImageDraw.Draw(page)
for i, ((w, h), (x, y)) in enumerate(zip(boxes, pos)):
    src = f"c{i + 1}.png"; im = fit(src, w, h)
    for cx, cy, lines, tail, size in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, size=size)
    page.paste(im, (x, y)); d.rectangle((x, y, x + w - 1, y + h - 1), outline=INK, width=2)
page.save("s48-2.png"); print(page.size)
