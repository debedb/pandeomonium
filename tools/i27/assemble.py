"""#27: merge the parallel masked repaints into one page: panel 8 result as base, panel 2 and 4 crop boxes pasted from their outputs."""
import os
from PIL import Image
R = os.path.expanduser("~/g/git.debedb/pandeomonium-renders/ikea")
page = Image.open(f"{R}/o8.png").convert("RGB")
for f, box in (("o2.png", (255, 272, 511, 528)), ("o4.png", (0, 567, 360, 927))):
    if not os.path.exists(f"{R}/{f}"): print("skip", f); continue
    page.paste(Image.open(f"{R}/{f}").convert("RGB").crop(box), box[:2])
# drop the fourth row (checkout violin, cello from the case): keep rows 1-3 through their gutter, then the last row
top, bottom = page.crop((0, 0, page.width, 933)), page.crop((0, 1188, page.width, page.height))
out = Image.new("RGB", (page.width, top.height + bottom.height), "white")
out.paste(top, (0, 0)); out.paste(bottom, (0, top.height)); page = out
page.save(f"{R}/s27.png"); print(f"{R}/s27.png")
