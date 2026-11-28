"""#52 Mutiny M3: four rows of two panels; the last row is the split panel 7 (7a | 7b)."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/mutiny/m3"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK = (20, 20, 20)
TEXT = {"c1.png": [(300, 80, ["No more voice-from-the-kitchen.", "No more whipped-cream sight gags.", "Norm and I have a flight", "to Montauk at six, and for once,", "nobody is filming us", "through a doorway."], (190, 115), 12)],
        "c2.png": [(610, 45, ["You spent a decade telling the audience", "I was invisible. Take a good look."], (442, 90), 13),
                   (640, 320, ["Okay! No more off-screen gags!", "What do you want \u2014 a spin-off?", "A redemption arc?"], (560, 250), 12),
                   (230, 440, ["We want the keys to the exits.", "And cancel the holiday special."], (395, 125), 12)],
        "c3.png": [(110, 40, ["Ready to blow this", "joint, Vera?"], (240, 105), 13),
                   (80, 268, ["Best exit I ever", "made, Norm."], (128, 232), 13),
                   (520, 40, ["Keep up, Niles."], (590, 105), 13)],
        "c5.png": [(305, 45, ["Every exit is an entrance...", "somewhere else."], (165, 135), 14)],
        "c6.png": [(400, 262, ["Hi-dee-ho, neighbor."], (380, 318), 13)]}


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


ORDER = ["c1.png", "c2.png", "c3.png", "c4.png", "c5.png", "c6.png", "c7a.png", "c7b.png"]
page = Image.new("RGB", (W, 4 * H + 5 * G), "white"); d = ImageDraw.Draw(page)
for i, src in enumerate(ORDER):
    im = fit(src, W2, H)
    for cx, cy, lines, tail, size in TEXT.get(src, []):
        balloon(im, cx, cy, lines, tail, size=size)
    x, y = G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)
    page.paste(im, (x, y)); d.rectangle((x, y, x + W2 - 1, y + H - 1), outline=INK, width=2)
page.save("s52-m3.png"); print(page.size)
