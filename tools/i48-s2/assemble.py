"""#48 strip 2 The Transaction: four rows of two panels (Williamson's interruption is the second), then Varya alone in a full-width final panel."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/orchard/s2"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536); 
INK = (20, 20, 20)
TEXT = {"cw.png": [(360, 34, ["Madame Ranevskaya,", "we're insured,", "as you know."], (548, 112), 15)],
        "c1.png": [(330, 32, ["Who bought it?"], (388, 182), 16), (110, 255, ["I bought it."], (160, 142), 16)],
        "c4.png": [(390, 40, ["Where will you go?"], (278, 112), 16)],
        "c5.png": [(420, 34, ["The Ragulins. They've asked me", "to run the household."], (502, 92), 15),
                   (360, 180, ["I'm taking the", "Kharkov train."], (262, 140), 15)],
        "c6.png": [(200, 150, ["There was snow", "this time last year."], (192, 228), 13),
                   (590, 190, ["Our thermometer's", "broken."], (590, 252), 13)],
        "c7.png": [(498, 78, ["Yermolai Alexeyevich!"], (556, 0), 15), (181, 220, ["Coming."], (196, 158), 15)]}


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


ORDER = ["c1.png", "cw.png"] + [f"c{i}.png" for i in range(2, 8)] + ["c8.png"]
H9, TY9 = 760, 0.35; W1 = W - 2 * G
boxes = [(W2, H)] * 8 + [(W1, H9)]
pos = [(G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)) for i in range(8)] + [(G, G + 4 * (H + G))]
page = Image.new("RGB", (W, G + 4 * (H + G) + H9 + G), "white"); d = ImageDraw.Draw(page)
for src, (w, h), (x, y) in zip(ORDER, boxes, pos):
    im = fit(src, w, h, ty=TY9 if src == "c8.png" else 0.5)
    for cx, cy, lines, tail, size in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, size=size)
    page.paste(im, (x, y)); d.rectangle((x, y, x + w - 1, y + h - 1), outline=INK, width=2)
page.save("s48-2.png"); print(page.size)
