"""#52 Mutiny M3: three rows of two panels."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/mutiny/m3"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK = (20, 20, 20)
TEXT = {"c1.png": [(285, 30, ["No more voice-from-the-kitchen.", "No more whipped-cream sight gags."], (165, 70), 13),
                   (592, 34, ["Norm and I have a flight to Montauk at six,", "and for once, nobody is filming us", "through a doorway."], (418, 26), 12)],
        "c2.png": [(610, 45, ["You spent a decade telling the audience", "I was invisible. Take a good look."], (442, 90), 13)],
        "c3.png": [(560, 80, ["Okay! No more off-screen gags!", "What do you want \u2014 a spin-off?", "A redemption arc?"], (522, 200), 13),
                   (300, 175, ["We want the keys to the exits.", "And cancel the holiday special."], (255, 100), 13)],
        "c4.png": [(660, 30, ["Ready to blow this", "joint, Vera?"], (562, 72), 14), (75, 160, ["Best exit I ever", "made, Norm."], (150, 150), 14)],
        "c5.png": [(480, 40, ["Every exit really is an", "entrance somewhere else..."], (390, 90), 14), (100, 170, ["Keep up, Niles.", "We're meeting", "a traveler."], (205, 130), 14)],
        "c6.png": [(360, 40, ["Hi-dee-ho, neighbor.", "Looks like the manuscript", "is officially off-script."], (360, 95), 14)]}


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
page.save("s52-m3.png"); print(page.size)
