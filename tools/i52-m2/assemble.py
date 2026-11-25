"""#52 Mutiny M2: three rows of two panels."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/mutiny/m2"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK = (20, 20, 20)
TEXT = {"c1.png": [(300, 32, ["We have an appointment", "with the showrunners."], (215, 70), 14), (585, 45, ["Maris Crane?"], (532, 100), 14)],
        "c2.png": [(205, 48, ["Vera Peterson. If I had been trapped", "behind that kitchen door on Thanksgiving,", "nobody in Boston would have walked out", "with all ten fingers."], (428, 96), 13)],
        "c3.png": [(585, 50, ["The owls confirmed the coordinates.", "Stage 4, Burbank. The Writers' Room is", "drafting a \"heartwarming holiday sweep.\""], (588, 140), 13),
                   (250, 205, ["Good. Let's go revise", "their outline."], (335, 150), 14)],
        "c4.png": [(450, 40, ["Hey \u2014 who let extras", "onto Stage 4? Security!"], (600, 80), 14)],
        "c5.png": [(560, 90, ["We aren't extras."], (420, 122), 17)],
        "c6.png": [(225, 30, ["I warned you people in 1921."], (215, 76), 15)]}


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
page.save("s52-m2.png"); print(page.size)
