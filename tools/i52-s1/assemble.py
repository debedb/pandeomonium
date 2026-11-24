"""#52 The Cranes strip 1: three rows of two panels."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/cranes/s1"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK = (20, 20, 20)
TEXT = {"c1.png": [(400, 24, ["Frasier!"], (412, 62), 16), (312, 98, ["Sam."], (286, 112), 16),
                   (655, 340, ["...before we get to the first class..."], (606, 296), 11)],
        "c2.png": [(300, 32, ["Those owls are watching us."], (362, 135), 15), (160, 100, ["They're looking through a window."], (150, 138), 15)],
        "c3.png": [(520, 40, ["There are two of them."], (545, 122), 15), (300, 82, ["And two of us.", "Please leave Jung out of this."], (300, 112), 15)],
        "c4.png": [(630, 168, ["Out of what?"], (628, 225), 16)],
        "c5.png": [(300, 45, ["Surely this isn't", "mere coincidence."], (305, 105), 15), (600, 52, ["Which part?"], (610, 95), 16)],
        "c6.png": [(230, 60, ["Do we know a Crane?"], (240, 165), 16), (480, 215, ["Which one?"], (372, 280), 16)]}


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
page.save("s52-1.png"); print(page.size)
