"""#1 strip 1 (Draw It Again): six square panels, 3x2, lettered."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw
from balloon212 import balloon
G, S = 6, 504
page = Image.new("RGB", (3 * S + 4 * G, 2 * S + 3 * G), "white")
d = ImageDraw.Draw(page)
cells = ["c1-a.png", "c2-a.png", "c3-a.png", "c4-a.png", "c5-a.png", "c6-b.png"]
for k, src in enumerate(cells):
    im = Image.open(src).convert("RGB").resize((S, S), Image.LANCZOS)
    if k == 0:
        balloon(im, 250, 52, ["Sam, she's not coming", "through that door."], (330, 128), size=16)
    if k == 3:
        balloon(im, 215, 62, ["Draw it again.", "DRAW IT AGAIN!"], (262, 222), size=17)
    if k == 5:
        balloon(im, 290, 34, ["What color is the boathouse", "at Hereford?"], (440, 235), size=15)
        balloon(im, 100, 112, ["HOW THE FUCK", "SHOULD I KNOW?"], (80, 140), size=15)
    x, y = G + (k % 3) * (S + G), G + (k // 3) * (S + G)
    page.paste(im, (x, y))
    d.rectangle((x, y, x + S - 1, y + S - 1), outline=(20, 20, 20), width=2)
page.save("s1-1.png")
