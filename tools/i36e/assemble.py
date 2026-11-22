"""#36 engineering deck: three rows of two panels plus a full-width holodeck panel; Euler and Geordi in the house serif."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/enterprise/eng"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
TEXT = {"c1.png": [(620, 36, ["So this is the backbone."], (560, 78), 17, False)],
        "c2.png": [(300, 40, ["Layer 2 or Layer 3?"], (200, 105), 17, False)],
        "c3.png": [(345, 40, ["I'm studying for my CCIE."], (225, 110), 16, False)],
        "c4.png": [(345, 40, ["You deliberately", "added cycles?"], (255, 105), 16, False),
                   (655, 34, ["For redundancy."], (560, 82), 16, False)],
        "c5.png": [(300, 40, ["Then you", "disable them?"], (185, 100), 16, False),
                   (662, 34, ["With spanning tree."], (562, 72), 15, False)],
        "c6.png": [(530, 32, ["What do you mean, VLANs???"], (300, 110), 17, False)],
        "c7.png": [(640, 52, ["Computer, show us the topology", "as a physical environment."], (440, 150), 17, False)]}


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


def letter(im, src):
    for cx, cy, lines, tail, size, it in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, italic=it, size=size)


page = Image.new("RGB", (W, 4 * H + 5 * G), "white"); d = ImageDraw.Draw(page)
for i in range(6):
    src = f"c{i + 1}.png"; im = fit(src, W2, H); letter(im, src)
    x, y = G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)
    page.paste(im, (x, y)); d.rectangle((x, y, x + W2 - 1, y + H - 1), outline=(20, 20, 20), width=2)
im = fit("c7.png", W - 2 * G, H, ty=0.1); letter(im, "c7.png"); x, y = G, G + 3 * (H + G)
page.paste(im, (x, y)); d.rectangle((x, y, x + W - 2 * G - 1, y + H - 1), outline=(20, 20, 20), width=2)
page.save("s36e.png"); print(page.size)
