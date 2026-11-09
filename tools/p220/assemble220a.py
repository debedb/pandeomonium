"""hq#217 cont.: strip A (Your mission...) - the call row from s220-1 plus the owls-and-Giant panel."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw
from balloon212 import balloon
top = Image.open("s220-1.png").crop((0, 0, 1536, 412))
g = Image.open("giant-a.png").convert("RGB").crop((0, 30, 1536, 800)).resize((1524, 764), Image.LANCZOS)
balloon(g, 290, 215, ["Very well. Make it so.", "Dismissed."], (450, 300), size=19)
page = Image.new("RGB", (1536, 412 + 6 + 764 + 6), "white")
page.paste(top, (0, 0)); page.paste(g, (6, 418))
ImageDraw.Draw(page).rectangle((6, 418, 1529, 418 + 763), outline=(20, 20, 20), width=2)
page.save("s220-1a.png")
