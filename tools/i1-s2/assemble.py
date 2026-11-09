"""#1 strip 2 (bathroom window): rows of 3/2/2 panels, no dialogue."""
from PIL import Image, ImageDraw
G, W = 6, 1536
W3, W2, H = 504, (W - 3 * G) // 2, 504
rows = [("c1-a.png", "c2-a.png", "c3-a.png"), ("c4-b.png", "c5-a.png"), ("c6-b.png", "c7-a.png")]
page = Image.new("RGB", (W, 3 * H + 4 * G), "white")
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
        page.paste(fit(src, w, H), (x, y))
        d.rectangle((x, y, x + w - 1, y + H - 1), outline=(20, 20, 20), width=2)
page.save("s1-2.png")
