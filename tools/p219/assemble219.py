"""hq#217: assemble strips 1 and 2 (new panel 9, recoloured page + pan-out) and letter their balloons."""
import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image, ImageDraw
from balloon212 import balloon
# strip 1: replace panel 9 with the standalone agent panel
s = Image.open("ref-swiss.png").convert("RGB")
p = Image.open("p9-b.png").convert("RGB").crop((0, 80, 1536, 717)).resize((844, 350), Image.LANCZOS)
s.paste(p, (690, 672))
balloon(s, 1345, 712, ["Вы ошиблись", "номером, дружище."], (1225, 765), size=17)
balloon(s, 1390, 815, ["Вы ошиблись", "номером."], (1250, 800), size=17)
balloon(s, 1420, 905, ["Вы ошиблись."], (1290, 860), size=17)
s.save("s219-1.png")
# strip 2: recoloured page, English lines, wide pan-out panel underneath
m = Image.open("met-a.png").convert("RGB")
balloon(m, 715, 440, ["This is my", "apartment!"], (640, 500), size=18)
balloon(m, 1030, 450, ["Of course.", "As a matter of fact,", "I'm there right now."], (1130, 500), size=17)
balloon(m, 290, 735, ["Who are you?"], (240, 790), size=18)
balloon(m, 1440, 790, ["Who?", "Who?"], (1385, 835), size=19)
H = 560
page = Image.new("RGB", (1536, 1024 + 8 + H), "white")
page.paste(m, (0, 0))
pan = Image.open("pan-a.png").convert("RGB").crop((0, 120, 1536, 120 + H))
page.paste(pan.crop((4, 0, 1532, H)), (4, 1032))
ImageDraw.Draw(page).rectangle((4, 1032, 1531, 1032 + H - 1), outline=(20, 20, 20), width=2)
page.crop((0, 0, 1536, 1032 + H + 4)).save("s219-2.png")
