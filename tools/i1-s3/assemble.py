"""#1 strip 3 (Bond / two Qs / directors): rows of 2 wide, 2 wide, then narrow + extra-wide."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw
from balloon212 import balloon
G, W, H = 6, 1536, 504
W2 = (W - 3 * G) // 2
WN = 504
WX = W - 3 * G - WN
rows = [[("c1-a.png", W2), ("c2-a.png", W2)], [("c3-a.png", W2), ("c4-a.png", W2)], [("c5-a.png", WN), ("c6-a.png", WX)]]
# balloons per panel, in panel coordinates: (cx, cy, lines, tail_xy)
TEXT = {
    "c3-a.png": [(150, 40, ["I am Q!"], (170, 150)), (600, 40, ["I am Q!"], (590, 150))],
    "c6-a.png": [(800, 52, ["Stop pointing the guns", "at my dads!"], (655, 150))],
}
page = Image.new("RGB", (W, len(rows) * H + (len(rows) + 1) * G), "white")
d = ImageDraw.Draw(page)
def fit(src, w, h):
    im = Image.open(src).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))
for r, row in enumerate(rows):
    x = G
    for src, w in row:
        y = G + r * (H + G)
        im = fit(src, w, H)
        for cx, cy, lines, tail in TEXT.get(src, []):
            balloon(im, cx, cy, lines, tail, size=17)
        page.paste(im, (x, y))
        d.rectangle((x, y, x + w - 1, y + H - 1), outline=(20, 20, 20), width=2)
        x += w + G
page.save("s1-3.png")
