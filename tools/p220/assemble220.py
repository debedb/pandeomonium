"""hq#217 cont.: rebuild Open this gate - new studio tile, Brandenburg Gate panels 3-7 - then blur Reagan and letter."""
import os, sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw, ImageFilter
from balloon212 import balloon
b = Image.open("gate-a.png").convert("RGB")
tile = "tile5-d.png"
b.paste(Image.open(tile).convert("RGB").crop((296, 207, 585, 378)), (296, 207))
def put(src, crop, box):
    w, h = box[2] - box[0], box[3] - box[1]
    b.paste(Image.open(src).convert("RGB").crop(crop).resize((w, h), Image.LANCZOS), box[:2])
put("p3-b.png", (10, 105, 1526, 976), (6, 415, 508, 703))
put("p4-b.png", (10, 105, 1526, 976), (511, 415, 1023, 703))
put("p345-e.png", (393, 10, 968, 338), (1027, 415, 1530, 703))
put("p345-e.png", (282, 349, 1078, 679), (6, 707, 754, 1017))
put("p345-e.png", (270, 689, 1092, 1015), (758, 707, 1530, 1017))
for box, r in (((1318, 10, 1528, 408), 6), ((175, 210, 290, 335), 3)):
    m = Image.new("L", b.size, 0); ImageDraw.Draw(m).rectangle(box, fill=255)
    b.paste(b.filter(ImageFilter.GaussianBlur(r)), (0, 0), m.filter(ImageFilter.GaussianBlur(8)))
balloon(b, 1130, 42, ["Mission accepted."], (1125, 95), size=18)
balloon(b, 190, 600, ["Meow."], (222, 650), size=16)
balloon(b, 330, 600, ["Meow."], (283, 650), size=16)
balloon(b, 640, 455, ["Mr. Gorbachev,", "open this gate."], (720, 560), size=16)
b.save("s220-1.png")
