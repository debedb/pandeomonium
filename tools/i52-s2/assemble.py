"""#52 The Cranes strip 2: three rows of two panels."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/cranes/s2"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK = (20, 20, 20)
TEXT = {"c1.png": [(200, 28, ["Where were you?"], (262, 95), 15), (470, 52, ["At the beach."], (505, 140), 15),
                   (150, 100, ["During work?"], (245, 120), 15), (610, 110, ["Whose?"], (538, 165), 15)],
        "c2.png": [(110, 30, ["Your crane fell."], (215, 75), 15), (430, 60, ["Mine?"], (520, 135), 15),
                   (110, 92, ["Yours!"], (212, 105), 15), (665, 85, ["Since when?"], (592, 150), 15)],
        "c3.png": [(110, 40, ["This morning."], (230, 100), 15), (420, 48, ["Before the beach", "or after?"], (482, 140), 15),
                   (140, 112, ["Before you came back!"], (232, 135), 15), (650, 140, ["So after I went."], (548, 180), 15)],
        "c4.png": [(115, 45, ["You should have", "been here."], (240, 110), 15), (520, 48, ["Earlier?"], (510, 122), 15),
                   (110, 132, ["Yes!"], (236, 140), 15), (650, 108, ["Then why are you", "asking me now?"], (562, 160), 15)],
        "c5.png": [(110, 32, ["Will you answer", "the question?"], (190, 90), 15), (420, 40, ["Which question?"], (530, 140), 15),
                   (345, 112, ["The one I just asked!"], (258, 122), 15), (630, 102, ["You asked whether I'd", "answer. I will."], (575, 142), 15)],
        "c6.png": [(120, 40, ["I'm asking about", "the crane!"], (245, 95), 15), (430, 42, ["And I'm telling you", "about the beach."], (540, 115), 15),
                   (140, 135, ["The beach is", "irrelevant!"], (245, 140), 15), (420, 200, ["Then why did you ask", "where I was?"], (522, 172), 15)]}


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
page.save("s52-2.png"); print(page.size)
