"""hq#217: overlay a fading French-horn phrase (staff fragment + notes) and bell sound arcs on the Italy strip."""
import math
from PIL import Image, ImageDraw
CREAM, INK = (250, 246, 236), (20, 20, 20)
def phrase(img, p0, p1, bend, scale, alpha):
    """Staff fragment along a quadratic curve p0->p1 (control point offset `bend`), with eighth notes riding it."""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cx, cy = (p0[0] + p1[0]) / 2 + bend[0], (p0[1] + p1[1]) / 2 + bend[1]
    pt = lambda t: ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * cx + t * t * p1[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * cy + t * t * p1[1])
    gap = 5 * scale; a = int(255 * alpha)
    for k in range(-2, 3):
        pts = [(x, y + k * gap) for x, y in (pt(i / 40) for i in range(41))]
        d.line(pts, fill=CREAM + (int(a * .8),), width=max(1, int(1.6 * scale)))
    heads = [(.12, 1), (.25, -1), (.38, 0), (.52, 2), (.66, -1), (.8, 1), (.92, 0)]
    for i, (t, step) in enumerate(heads):
        x, y = pt(t); y += step * gap
        rx, ry = 4.2 * scale, 3.1 * scale
        d.ellipse((x - rx - 1, y - ry - 1, x + rx + 1, y + ry + 1), fill=INK + (a,))
        d.ellipse((x - rx, y - ry, x + rx, y + ry), fill=CREAM + (a,))
        d.line((x + rx - 1, y, x + rx - 1, y - 22 * scale), fill=CREAM + (a,), width=max(2, int(2 * scale)))
        if i % 2 == 0 and i + 1 < len(heads):  # beam pairs
            x2, y2 = pt(heads[i + 1][0]); y2 += heads[i + 1][1] * gap
            d.line((x + rx - 1, y - 22 * scale, x2 + rx - 1, y2 - 22 * scale), fill=CREAM + (a,), width=max(3, int(4 * scale)))
    img.alpha_composite(lay)
def bell_arcs(img, c, r0, n, alpha, span=(140, 220)):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(n):
        r = r0 + k * 18
        d.arc((c[0] - r, c[1] - r, c[0] + r, c[1] + r), span[0], span[1], fill=CREAM + (int(255 * alpha * (1 - k / (n + 1))),), width=4)
    img.alpha_composite(lay)
im = Image.open("it-b3.png").convert("RGBA")
phrase(im, (1405, 215), (1180, 60), (30, -40), 1.25, .95)   # panel 3: horn loud
phrase(im, (372, 785), (490, 690), (-20, -25), .8, .7)      # panel 4: quieter
phrase(im, (930, 805), (860, 760), (0, -10), .45, .4)        # panel 5: almost gone
bell_arcs(im, (1375, 725), 70, 4, .9)                         # panel 6: the bell takes over
bell_arcs(im, (1375, 725), 70, 3, .6, (300, 20))
im.convert("RGB").save("s217-1.png")
