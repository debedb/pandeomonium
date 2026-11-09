"""#1 strip 2 (bathroom window): rows of 2/3/2/2 panels; only the cafe opener is lettered."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw
from balloon212 import balloon
G, W = 6, 1536
W3, W2, H = 504, (W - 3 * G) // 2, 504
rows = [("c0a.png", "c0b.png"), ("c1-a.png", "c2-a.png", "c3-a.png"), ("c4-b.png", "c5-a.png"), ("c6-b.png", "c7-a.png")]
# balloons per panel, in panel coordinates: (cx, cy, lines, tail_xy)
TEXT = {
    "c0a.png": [(190, 44, ["She's not coming through", "that door, Sam."], (190, 205)),
                (590, 104, ["Let it be.", "It won't be long."], (690, 240))],
    "c0b.png": [(340, 26, ["Excuse me."], (246, 104))],
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
    w = W3 if len(row) == 3 else W2
    for k, src in enumerate(row):
        x, y = G + k * (w + G), G + r * (H + G)
        im = fit(src, w, H)
        for cx, cy, lines, tail in TEXT.get(src, []):
            balloon(im, cx, cy, lines, tail, size=16)
        page.paste(im, (x, y))
        d.rectangle((x, y, x + w - 1, y + H - 1), outline=(20, 20, 20), width=2)
page.save("s1-2.png")
