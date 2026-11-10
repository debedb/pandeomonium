"""#24 real estate office: two rows of two wide panels, then Kant full width."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw
from balloon212 import balloon
G, W = 6, 1536
W2, H = (W - 3 * G) // 2, 504
WF, HF = W - 2 * G, 800
rows = [[("c1-a.png", W2, H), ("c2-a.png", W2, H)],
        [("c3-a.png", W2, H), ("c4-a.png", W2, H)],
        [("c5-a.png", WF, HF)]]
TY = {"c5-a.png": 0.15}
# balloons per panel, in panel coordinates: (cx, cy, lines, tail_xy, size, italic)
TEXT = {
    "c1-a.png": [(470, 44, ["You see this watch? You see this watch?", "That watch costs more than your car."], (276, 160), 16, False)],
    "c2-a.png": [(450, 62, ["Ma gavte la nata!"], (414, 214), 14, True)],
    "c4-a.png": [(500, 50, ["It wasn't the cork.", "It was this watch!"], (306, 120), 17, False)],
}
page = Image.new("RGB", (W, sum(r[0][2] for r in rows) + (len(rows) + 1) * G), "white")
d = ImageDraw.Draw(page)
def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))
y = G
for row in rows:
    x = G
    for src, w, h in row:
        im = fit(src, w, h, TY.get(src, 0.5))
        for cx, cy, lines, tail, size, it in TEXT.get(src, []):
            balloon(im, cx, cy, lines, tail, italic=it, size=size)
        page.paste(im, (x, y))
        d.rectangle((x, y, x + w - 1, y + h - 1), outline=(20, 20, 20), width=2)
        x += w + G
    y += row[0][2] + G
page.save("s24.png")
