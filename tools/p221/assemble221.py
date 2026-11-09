"""hq#217 cont.: What's in the case??? - eight square panels in rows of 3/3/2, lettered."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw
from balloon212 import balloon
G, W3, H = 6, 504, 504
W2 = (1536 - 3 * G) // 2
page = Image.new("RGB", (1536, 3 * H + 4 * G), "white")
d = ImageDraw.Draw(page)
def put(src, x, y, w, h):
    im = Image.open(src).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((l, t, l + w, t + h))
    return im
cells = []
for r, row in enumerate((("c1-c.png", "c2-a.png", "c3-b.png"), ("c4-b.png", "c5-a.png", "c6-b.png"), ("c7-b.png", "c8-a.png"))):
    w = W3 if len(row) == 3 else W2
    for k, src in enumerate(row):
        x, y = G + k * (w + G), G + r * (H + G)
        im = put(src, x, y, w, H)
        if src == "c3-b.png":
            balloon(im, 295, 112, ["Where's Gregor?"], (345, 172), size=16)
            balloon(im, 115, 162, ["Gregor fucked us!"], (120, 192), size=16)
        if src == "c7-b.png":
            balloon(im, 600, 30, ["An unexplained", "phenomenon, sir."], (600, 92), size=16)
            balloon(im, 235, 50, ["Well, we'd better", "explain it, then!"], (240, 82), size=16)
        page.paste(im, (x, y))
        d.rectangle((x, y, x + w - 1, y + H - 1), outline=(20, 20, 20), width=2)
page.save("s221-1.png")
