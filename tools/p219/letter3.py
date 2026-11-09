"""hq#217 strip 3: letter the owls' and Asya's balloons onto meet-a.png."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image
from balloon212 import balloon
b = Image.open("meet-a.png").convert("RGB")
balloon(b, 850, 48, ["Comment сова?"], (800, 125), size=17)
balloon(b, 1075, 40, ["Филин good."], (1085, 82), size=17)
balloon(b, 1420, 42, ["They're late."], (1425, 88), size=17)
balloon(b, 760, 560, ["The humans", "suspect nothing."], (620, 740), size=18)
b.save("s219-3.png")
