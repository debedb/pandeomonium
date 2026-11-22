"""#36 ready room: four rows of two panels; English balloons in the house serif, Joshua's line in Hebrew (RTL via raqm)."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw, ImageFont
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/enterprise"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK, CREAM = (20, 20, 20), (250, 246, 236)
HE = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"


def he_balloon(img, cx, cy, text, tail, size=28):
    """A balloon with one right-to-left Hebrew line, nikud shaped by raqm."""
    d = ImageDraw.Draw(img); f = ImageFont.truetype(HE, size)
    w = d.textlength(text, font=f, direction="rtl", language="he")
    bw, bh = w + 2 * size, size * 2.2
    base = [(cx - bw * .12, cy + bh / 2 - 4), (cx + bw * .06, cy + bh / 2 - 4)]
    d.polygon(base + [tail], fill=CREAM, outline=INK)
    d.rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), radius=bh / 2, fill=CREAM, outline=INK, width=2)
    d.polygon([(base[0][0] + 2, base[0][1] - 3), (base[1][0] - 2, base[1][1] - 3), (tail[0], tail[1] - 4)], fill=CREAM)
    d.text((cx, cy), text, font=f, fill=INK, anchor="mm", direction="rtl", language="he")


TEXT = {"c2.png": [(560, 46, ["Professor, would you join me", "in my ready room?"], (500, 112), 16, False)],
        "c5.png": [(377, 36, ["Rabbi, Professor, this is", "something we need to discuss."], (380, 70), 16, False)],
        "c6.png": [(150, 36, ["Captain, if I may..."], (190, 68), 17, False)],
        "c8.png": [(650, 40, ["Oh, shut up, Wesley."], (565, 85), 17, False)]}
HEB = {"c3.png": (600, 40, "לֹא בַשָּׁמַיִם הִוא", (455, 125))}


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
    if src in HEB:
        cx, cy, t, tail = HEB[src]; he_balloon(im, cx, cy, t, tail)
    x, y = G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)
    page.paste(im, (x, y)); d.rectangle((x, y, x + W2 - 1, y + H - 1), outline=INK, width=2)
page.save("s36.png"); print(page.size)
