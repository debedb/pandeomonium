"""#1 strip 3 (Bond / two Qs / directors): three rows of two wide panels, then the standoff full width."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw
from balloon212 import balloon
G, W = 6, 1536
W2, H = (W - 3 * G) // 2, 504
WF, HF = W - 2 * G, 760
rows = [[("n1.png", W2, H), ("n2.png", W2, H)],
        [("c3-a.png", W2, H), ("n4.png", W2, H)],
        [("n5.png", W2, H), ("n6.png", W2, H)],
        [("c6-a.png", WF, HF)]]
# balloons per panel, in panel coordinates: (cx, cy, lines, tail_xy)
TEXT = {
    "c3-a.png": [(150, 40, ["I am Q!"], (170, 150)), (600, 40, ["I am Q!"], (590, 150))],
    "c6-a.png": [(1200, 70, ["Stop pointing the guns", "at my dads!"], (986, 210))],
}
page = Image.new("RGB", (W, sum(r[0][2] for r in rows) + (len(rows) + 1) * G), "white")
d = ImageDraw.Draw(page)
def fit(src, w, h):
    im = Image.open(src).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))
y = G
for row in rows:
    x = G
    for src, w, h in row:
        im = fit(src, w, h)
        for cx, cy, lines, tail in TEXT.get(src, []):
            balloon(im, cx, cy, lines, tail, size=17 if src != "c6-a.png" else 20)
        page.paste(im, (x, y))
        d.rectangle((x, y, x + w - 1, y + h - 1), outline=(20, 20, 20), width=2)
        x += w + G
    y += row[0][2] + G
page.save("s1-3.png")
