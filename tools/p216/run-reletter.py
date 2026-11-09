import sys; sys.path.insert(0, "../pandeomonium")
from PIL import Image
from reletter216 import reletter
im = Image.open("ref-creole.png").convert("RGB")
H = lambda t: [(t, "he")]
reletter(im, (245, 115), [H("אין װעלכער שעה"), [("pidgin", "la-i"), (" ", "la"), ("װערט אַ", "he")], [("?creole", "la-i"), (" ", "la"), ("אַ", "he")]], size=30, center=(328, 72))
reletter(im, (992, 65), [H("און װען װערט"), H("אַ דיאַלעקט"), H("אַ שפּראַך?")], size=31, center=(1100, 62))
reletter(im, (242, 430), [H("װוּ איז"), H("מײַן פֿלאָט?")], size=32, center=(326, 428))
reletter(im, (320, 737), [H("איצט איז עס"), H("אַ שפּראַך.")], size=32, center=(322, 738))
reletter(im, (1190, 742), [H("שפּעט.")], size=40, center=(1190, 773))
im.save("s216-1.png")
im.crop((180,0,700,180)).resize((1040,360)).save('/private/tmp/claude-501/-Users-gregory-g-manda-git-hq/e10f9e3c-c218-454c-a2be-3376a1f922c7/scratchpad/rel-b1.png')
