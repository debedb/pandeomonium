"""#14: paste the regenerated heaven panel (three-way high five) into the strip whose last dinner panel already has Scalia's white tie (wt2.png)."""
import os
from PIL import Image
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/scotus"))
strip = Image.open("wt2.png").convert("RGB")
box = (1300, 8, 1528, 524)  # panel 6 interior
w = round(1536 * (box[2] - box[0]) / (box[3] - box[1]))
p6 = Image.open("h6b2.png").convert("RGB").crop((170, 0, 170 + w, 1536)).resize((box[2] - box[0], box[3] - box[1]), Image.LANCZOS)
strip.paste(p6, box[:2]); strip.save("s14.png"); print("s14.png")
