"""#48 strip 5 Narrative Economy: two panels, a wide panel 3, the Jerry/Newman close-ups side by side, then the wide final panel."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/orchard/s5"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536); W1 = W - 2 * G; H3, H6 = 560, 720
INK = (20, 20, 20)
TEXT = {"c2.png": [(170, 34, ["Y'know, narrative economy was", "originally a postal regulation."], (212, 138), 14),
                   (395, 178, ["Exposition is short for", "\"express postage.\"", "Most people don't realize that."], (286, 200), 14)],
        "c3.png": [(540, 80, ["Your background information has to arrive", "before the story. Otherwise they hold", "the plot at the sorting office."], (752, 150), 15)],
        "c6.png": [(800, 58, ["Now, the sorting office itself requires a little", "background, because there were originally", "three classes of delivery..."], (832, 160), 15)]}
TY = {}


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


boxes = [(W2, H), (W2, H), (W1, H3), (W2, H), (W2, H), (W1, H6)]
y2 = 2 * G + H; y3 = y2 + H3 + G; y4 = y3 + H + G
pos = [(G, G), (2 * G + W2, G), (G, y2), (G, y3), (2 * G + W2, y3), (G, y4)]
page = Image.new("RGB", (W, y4 + H6 + G), "white"); d = ImageDraw.Draw(page)
for i, ((w, h), (x, y)) in enumerate(zip(boxes, pos)):
    src = f"c{i + 1}.png"; im = fit(src, w, h, ty=TY.get(src, 0.5))
    for cx, cy, lines, tail, size in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, size=size)
    page.paste(im, (x, y)); d.rectangle((x, y, x + w - 1, y + h - 1), outline=INK, width=2)
page.save("s48-5.png"); print(page.size)
