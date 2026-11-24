"""#52 Mutiny M1: three rows of two panels."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/mutiny/m1"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK = (20, 20, 20)
TEXT = {"c1.png": [(520, 45, ["Right on schedule, Vera.", "Norm just ordered his third mug, so you've got", "forty-two minutes of unscripted airtime."], (505, 136), 13)],
        "c2.png": [(420, 45, ["Ankles, a hemline, and a voice from", "the kitchen, Wilson. Not even a face."], (218, 96), 14)],
        "c3.png": [(480, 80, ["As the ancient Stoics observed, Vera,", "a shadow only looks flat because", "the lamp is bolted to the ceiling."], (500, 215), 14)],
        "c4.png": [(400, 42, ["Take this — the owls intercepted it over Seattle.", "You're not the only one", "the camera refused to shoot."], (350, 102), 13)],
        "c6.png": [(138, 62, ["For eleven seasons, Niles,", "they claimed I weighed less than", "a soufflé, couldn't cast a shadow, and", "sprained my wrist turning a butter knife."], (270, 112), 13),
                   (640, 40, ["And yet you possess", "the core strength of a Cirque", "du Soleil acrobat, my love."], (590, 86), 13)]}


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
page.save("s52-m1.png"); print(page.size)
