"""hq#211: lighten Landa's tunic to the film's grey-green by hand, without an image model. Usage: tunic211.py IN OUT"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
o = Image.open(sys.argv[1]).convert("RGB")
P = [(272,135),(235,160),(165,175),(120,240),(58,370),(60,395),(110,425),(125,372),(170,345),(215,365),(330,378),(385,372),(440,388),(492,375),(497,345),(440,285),(412,262),(405,232),(375,240),(340,200),(300,235),(270,215)]
pm = Image.new("L", o.size, 0); d = ImageDraw.Draw(pm)
d.polygon([(x + 890, y) for x, y in P], fill=255)
d.polygon([(x + 883, y + 505) for x, y in P], fill=255)
pm = np.asarray(pm.filter(ImageFilter.GaussianBlur(1.5)), float) / 255
a = np.asarray(o, float); v = a.max(2); s = (v - a.min(2)) / np.maximum(v, 1)
w = pm * np.clip((v - 14) / 16, 0, 1) * np.clip((185 - v) / 40, 0, 1) * np.clip((0.68 - s) / 0.12, 0, 1)
gain = np.array([1.55, 1.75, 1.8])
Image.fromarray(np.clip(a * (1 + w[..., None] * (gain - 1)), 0, 255).astype("uint8")).save(sys.argv[2])
