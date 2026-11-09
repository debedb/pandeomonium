"""hq#212: draw a cream speech balloon with a tail onto an image, in the house serif. Usage from Python: balloon(img, cx, cy, lines, tail_xy, italic=False, note=False, size=17)"""
from PIL import ImageDraw, ImageFont
F = "/System/Library/Fonts/Supplemental/Georgia{}.ttf"
SYM = "/System/Library/Fonts/Apple Symbols.ttf"
def balloon(img, cx, cy, lines, tail, italic=False, note=False, size=17):
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(F.format(" Italic" if italic else ""), size)
    sym = ImageFont.truetype(SYM, size + 4)
    lh = size + 4
    ws = [d.textlength(t, font=font) + (size + 2 if note and i == 0 else 0) for i, t in enumerate(lines)]
    w, h = max(ws) + 2 * size, lh * len(lines) + size
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    base = [(cx - w * .12, cy + h / 2 - 4), (cx + w * .06, cy + h / 2 - 4)]
    d.polygon(base + [tail], fill=(250, 246, 236), outline=(20, 20, 20))
    d.rounded_rectangle(box, radius=min(w, h) / 2, fill=(250, 246, 236), outline=(20, 20, 20), width=2)
    d.polygon([(base[0][0] + 2, base[0][1] - 3), (base[1][0] - 2, base[1][1] - 3), (tail[0], tail[1] - 4)], fill=(250, 246, 236))
    y = cy - lh * len(lines) / 2
    for i, t in enumerate(lines):
        x = cx - ws[i] / 2
        if note and i == 0:
            d.text((x, y - 3), "♪", font=sym, fill=(20, 20, 20)); x += size + 2
        d.text((x, y), t, font=font, fill=(20, 20, 20)); y += lh
