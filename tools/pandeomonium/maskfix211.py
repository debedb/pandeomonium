"""hq#211: regenerate only a masked region of a page with gpt-image-2 and feather-blend it into the original pixels. Usage: maskfix211.py SRC cx0 cy0 cx1 cy1 mx0 my0 mx1 my1 REF OUT PROMPT  (c* = crop sent to the model, m* = region to replace, page coords)"""
import base64, io, json, os, sys, urllib.request
from PIL import Image, ImageDraw, ImageFilter
a = sys.argv
src, (cx0, cy0, cx1, cy1), (mx0, my0, mx1, my1), ref, out, prompt = a[1], map(int, a[2:6]), map(int, a[6:10]), a[10], a[11], a[12]
page = Image.open(src).convert("RGB"); crop = page.crop((cx0, cy0, cx1, cy1)); S = 1024
sx, sy = S / crop.width, S / crop.height
mask = Image.new("RGBA", (S, S), (0, 0, 0, 255))
poly = [tuple(map(int, p.split(","))) for p in os.environ["POLY"].split()] if os.environ.get("POLY") else None  # page-coord "x,y x,y ..." overrides the m* box
if poly: ImageDraw.Draw(mask).polygon([((x - cx0) * sx, (y - cy0) * sy) for x, y in poly], fill=(0, 0, 0, 0))
else: ImageDraw.Draw(mask).rectangle(((mx0 - cx0) * sx, (my0 - cy0) * sy, (mx1 - cx0) * sx, (my1 - cy0) * sy), fill=(0, 0, 0, 0))
def png(im): buf = io.BytesIO(); im.save(buf, "PNG"); return buf.getvalue()
b = "----p211m"
body = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in (("model", "gpt-image-2"), ("prompt", prompt), ("size", f"{S}x{S}"), ("quality", "high")))
files = [("image[]", "crop.png", png(crop.resize((S, S), Image.LANCZOS)))] + ([("image[]", "ref.png", open(ref, "rb").read())] if ref != "-" else []) + [("mask", "mask.png", png(mask))]
for field, name, data in files:
    body += f'--{b}\r\nContent-Disposition: form-data; name="{field}"; filename="{name}"\r\nContent-Type: image/png\r\n\r\n'.encode() + data + b"\r\n"
body += f"--{b}--\r\n".encode()
req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, method="POST",
                             headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": f"multipart/form-data; boundary={b}"})
try:
    with urllib.request.urlopen(req, timeout=580) as r:
        data = json.load(r)["data"][0]["b64_json"]
except urllib.error.HTTPError as e:
    sys.exit(f"{out}: HTTP {e.code} {e.read().decode()[:500]}")
new = Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB").resize(crop.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(float(os.environ.get("SOFTEN", "0"))))
blend = Image.new("L", crop.size, 0)
if poly: ImageDraw.Draw(blend).polygon([(x - cx0, y - cy0) for x, y in poly], fill=255)
else: ImageDraw.Draw(blend).rectangle((mx0 - cx0, my0 - cy0, mx1 - cx0, my1 - cy0), fill=255)
blend = blend.filter(ImageFilter.GaussianBlur(float(os.environ.get("FEATHER", "10"))))
page.paste(Image.composite(new, crop, blend), (cx0, cy0)); page.save(out); print(out)
