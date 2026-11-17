"""#29 philosophers' football: three rows of two panels plus a full-width closer; commentator balloons from the booth on both substitutions, Eureka on Archimedes."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw, ImageFont
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/football"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
TEXT = {"c2.png": [(170, 34, ["A very controversial choice."], (330, 70), 16, False)],
        "c3.png": [(210, 38, ["Another controversial choice. Seems team", "managers today are doing everything unexpected."], (430, 60), 14, False)],
        "c4.png": [(560, 70, ["Eureka!"], (420, 190), 26, False)]}
CAPTION = {}
H7, TY7 = 900, 0.75
def caption(im, text, size=20):
    d = ImageDraw.Draw(im); f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", size)
    w = d.textlength(text, font=f) + 2 * size; h = size * 2
    d.rectangle((10, 10, 10 + w, 10 + h), fill=(250, 238, 190), outline=(20, 20, 20), width=2)
    d.text((10 + size, 10 + size / 2 - 1), text, font=f, fill=(20, 20, 20))
def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))
page = Image.new("RGB", (W, 3 * H + H7 + 5 * G), "white"); d = ImageDraw.Draw(page)
for i in range(6):
    src = f"c{i + 1}.png"; im = fit(src, W2, H)
    for cx, cy, lines, tail, size, it in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, italic=it, size=size)
    if src in CAPTION: caption(im, CAPTION[src])
    x, y = G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)
    page.paste(im, (x, y)); d.rectangle((x, y, x + W2 - 1, y + H - 1), outline=(20, 20, 20), width=2)
im = fit("c7.png", W - 2 * G, H7, TY7); y = G + 3 * (H + G)
page.paste(im, (G, y)); d.rectangle((G, y, W - G - 1, y + H7 - 1), outline=(20, 20, 20), width=2)
page.save("s29.png"); print(page.size)
