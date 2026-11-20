"""#34: three rows of two panels plus a full-width outro; one shout balloon for O'Reilly."""
import math, os, sys
sys.path.insert(0, os.path.expanduser("~/g/git.debedb/pandeomonium/tools/pandeomonium"))
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.expanduser("~/g/git.debedb/pandeomonium-renders/perl"))
G, W = 6, 1536
W2 = (W - 3 * G) // 2; H = round(W2 * 1024 / 1536)
INK, CREAM = (20, 20, 20), (250, 246, 236)


def burst(img, cx, cy, lines, tail, size=24):
    """A jagged shout balloon in Georgia Bold."""
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", size)
    lh = size + 6
    ws = [d.textlength(t, font=font) for t in lines]
    rx, ry = max(ws) / 2 + size * 1.3, lh * len(lines) / 2 + size * 1.1
    pts = []
    n = 22
    for k in range(2 * n):
        a = math.pi * k / n
        r = 1.0 if k % 2 == 0 else 0.82
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    d.polygon([(cx + rx * .1, cy + ry * .6), (cx + rx * .35, cy + ry * .5), tail], fill=CREAM, outline=INK)
    d.polygon(pts, fill=CREAM, outline=INK, width=3)
    d.polygon([(cx + rx * .12, cy + ry * .55), (cx + rx * .33, cy + ry * .45), (tail[0] - 3, tail[1] - 5)], fill=CREAM)
    y = cy - lh * len(lines) / 2
    for i, t in enumerate(lines):
        d.text((cx - ws[i] / 2, y), t, font=font, fill=INK); y += lh


def fit(src, w, h, ty=0.5):
    im = Image.open(src).convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, round((im.height - h) * ty)
    return im.crop((l, t, l + w, t + h))


SHOUT = {"c6.png": (395, 64, ["Fuck it!", "We'll do it live!"], (522, 114))}
page = Image.new("RGB", (W, 4 * H + 5 * G), "white"); d = ImageDraw.Draw(page)
for i in range(6):
    src = f"c{i + 1}.png"; im = fit(src, W2, H)
    if src in SHOUT:
        cx, cy, lines, tail = SHOUT[src]; burst(im, cx, cy, lines, tail)
    x, y = G + (i % 2) * (W2 + G), G + (i // 2) * (H + G)
    page.paste(im, (x, y)); d.rectangle((x, y, x + W2 - 1, y + H - 1), outline=INK, width=2)
im = fit("c7.png", W - 2 * G, H, ty=0.45); x, y = G, G + 3 * (H + G)
page.paste(im, (x, y)); d.rectangle((x, y, x + W - 2 * G - 1, y + H - 1), outline=INK, width=2)
page.save("s34.png"); print(page.size)
