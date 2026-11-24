"""#52 The Cranes strip 2: three rows of two panels."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw
from balloon212 import balloon
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/cranes/s2"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK = (20, 20, 20)
TEXT = {"c1.png": [(150, 45, ["Послушайте, Кольцов,", "вы, конечно, были", "на работе, да?"], (240, 108), 14), (560, 80, ["Да!"], (552, 150), 15),
                   (150, 175, ["А?"], (240, 165), 15), (665, 150, ["А?"], (592, 188), 15)],
        "c2.png": [(100, 30, ["Это что такое?"], (190, 55), 14), (650, 285, ["Что именно?"], (530, 195), 14),
                   (110, 100, ["Что у вас на шее?"], (195, 92), 14), (660, 350, ["На моей?"], (560, 235), 14)],
        "c3.png": [(420, 30, ["Это полотенце."], (540, 135), 14),
                   (320, 150, ["При чём тут полотенце?", "Да вы знаете, что у вас", "сегодня случилось?"], (200, 120), 13),
                   (672, 250, ["Ещё бы."], (605, 212), 14)],
        "c4.png": [(110, 34, ["Вас искали раньше,", "до нашего разговора!"], (185, 76), 13), (420, 92, ["Так «раньше»", "или «до того»?"], (530, 172), 13),
                   (100, 192, ["Раньше... Нет, до того."], (192, 142), 13), (690, 118, ["Раньше до или", "до раньше того?"], (622, 162), 13)],
        "c5.png": [(595, 58, ["Вот тут я не пойму:", "если вы спрашиваете,", "я буду отвечать. Если вы", "отвечаете, я буду спрашивать."], (610, 140), 13),
                   (110, 34, ["Пока я начальник,", "я спрашиваю!"], (215, 76), 13), (420, 250, ["Почему «пока»?"], (560, 205), 13)],
        "c6.png": [(130, 30, ["Да вы знаете, что случилось", "на вашем участке или нет?"], (175, 62), 13),
                   (650, 45, ["Стоп! Осторожно,", "у меня что-то с головой.", "Это порт?"], (590, 112), 13),
                   (90, 182, ["Порт."], (165, 150), 14)]}


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
