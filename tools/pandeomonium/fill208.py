"""hq#208: inpaint the transparent (background-removed) areas of a page via gpt-image-2, keep every opaque pixel. Usage: fill208.py SRC OUT PROMPT"""
import base64, io, json, os, sys, urllib.request
from PIL import Image, ImageFilter
src, out, prompt = sys.argv[1:4]
im = Image.open(src).convert("RGBA"); W, H = im.size
work = im.resize((1024, 1536), Image.LANCZOS)
flat = Image.new("RGB", work.size, "white"); flat.paste(work, mask=work.getchannel("A"))
mask = Image.new("RGBA", work.size, (0, 0, 0, 255)); mask.putalpha(work.getchannel("A").point(lambda v: 255 if v >= 250 else 0))
def png(i): b = io.BytesIO(); i.save(b, "PNG"); return b.getvalue()
B = "----p208"
def part(name, val): return f'--{B}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{val}\r\n'.encode()
def filepart(name, data): return f'--{B}\r\nContent-Disposition: form-data; name="{name}"; filename="{name}.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + data + b"\r\n"
body = part("model", "gpt-image-2") + part("prompt", prompt) + part("size", "1024x1536") + filepart("image[]", png(flat)) + filepart("mask", png(mask)) + f"--{B}--\r\n".encode()
req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, method="POST",
                             headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": f"multipart/form-data; boundary={B}"})
with urllib.request.urlopen(req, timeout=400) as r:
    gen = Image.open(io.BytesIO(base64.b64decode(json.load(r)["data"][0]["b64_json"]))).convert("RGB").resize((W, H), Image.LANCZOS)
gen.save(out.replace(".png", "-raw.png"))
keep = im.getchannel("A").filter(ImageFilter.GaussianBlur(1.5))
res = gen.copy(); res.paste(im.convert("RGB"), mask=keep); res.save(out); print(out)
