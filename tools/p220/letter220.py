"""hq#217 cont.: blur Reagan behind the cats (panel 2 and the call tile) and letter the Open this gate page."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw, ImageFilter
from balloon212 import balloon
b = Image.open("gate-a.png").convert("RGB")
for box, r in (((1318, 10, 1528, 408), 6), ((175, 210, 290, 335), 3)):
    m = Image.new("L", b.size, 0); ImageDraw.Draw(m).rectangle(box, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(8))
    b.paste(b.filter(ImageFilter.GaussianBlur(r)), (0, 0), m)
balloon(b, 1130, 42, ["Mission accepted."], (1125, 95), size=18)
balloon(b, 88, 495, ["Meow."], (150, 540), size=16)
balloon(b, 330, 495, ["Meow."], (262, 545), size=16)
balloon(b, 610, 455, ["Mr. Gorbachev,", "open this gate."], (600, 570), size=16)
b.save("s220-1.png")
