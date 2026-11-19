"""#31 cheese shop: four rows of two panels; lettering for Serling, Cleese and the shopkeeper."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/cheese"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
TEXT = {"c2.png": [(235, 52, ["You have already entered another dimension.", "A dimension of ..."], (440, 192), 15, False)],
        "c5.png": [(300, 42, ["Would you shut that bloody dancing up!"], (518, 98), 16, False)],
        "c6.png": [(140, 40, ["The cat's eaten it!"], (240, 90), 18, False)]}
def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))
page = Image.new("RGB", (W, 4 * H + 5 * G), "white"); d = ImageDraw.Draw(page)
for i in range(8):
    src = f"c{i + 1}.png"; im = fit(src, W2, H)
    for cx, cy, lines, tail, size, it in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, italic=it, size=size)
    x, y = G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)
    page.paste(im, (x, y)); d.rectangle((x, y, x + W2 - 1, y + H - 1), outline=(20, 20, 20), width=2)
page.save("s31.png"); print(page.size)
