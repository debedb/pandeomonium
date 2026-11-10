"""#1 strip 4 (Sonnet 18 / author / Solomon): three square-ish panels, then the author beside the serenade, then Solomon full width, then the coda (author gone, the secret chord, she returns)."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw
from balloon212 import balloon
G, W = 6, 1536
W3, H1 = (W - 4 * G) // 3, 420
W4, H2 = 380, 480
W5 = W - 3 * G - W4
WF, HF = W - 2 * G, 880
rows = [[("c1-a.png", W3, H1), ("c2-a.png", W3, H1), ("c3-a.png", W3, H1)],
        [("c4-a.png", W4, H2), ("c5-a.png", W5, H2)],
        [("c6-a.png", WF, HF)],
        [("c7-a.png", W3, W3), ("c8-a.png", W3, W3), ("c9-a.png", W3, W3)]]
# balloons per panel, in panel coordinates: (cx, cy, lines, tail_xy, size)
TEXT = {
    "c4-a.png": [(265, 90, ["18."], (150, 190), 34)],
    "c5-a.png": [(400, 60, ["Shall I compare thee to a summer's day?",
                            "Thou art more lovely and more temperate..."], (212, 178), 19)],
    "c8-a.png": [(165, 52, ["I'll show you a secret chord", "my father played."], (252, 228), 18)],
    "c6-a.png": [(640, 300, ["This too shall pass."], (905, 420), 26)],
}
THOUGHT = {"c5-a.png": [(985, 150, ["That's what", "Barbara Cartland", "said."], (950, 300), 18)]}
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
        im = fit(src, w, h, 0.1 if src == "c6-a.png" else 0.5)
        for cx, cy, lines, tail, size in TEXT.get(src, []):
            balloon(im, cx, cy, lines, tail, size=size)
        for cx, cy, lines, tail, size in THOUGHT.get(src, []):
            balloon(im, cx, cy, lines, (cx, cy), size=size)
            dd = ImageDraw.Draw(im)
            for k, r in enumerate((9, 6, 4)):
                bx = cx + (tail[0] - cx) * (k + 1) / 3.5
                by = cy + 55 + (tail[1] - cy - 55) * (k + 1) / 3.5
                dd.ellipse((bx - r, by - r, bx + r, by + r), fill="white", outline="black", width=2)
        page.paste(im, (x, y))
        d.rectangle((x, y, x + w - 1, y + h - 1), outline=(20, 20, 20), width=2)
        x += w + G
    y += row[0][2] + G
page.save("s1-4.png")
