"""hq#211: redraw one panel with gpt-image-2, matching characters to a reference image, and paste it back. Usage: refpanel211.py SRC x0 y0 x1 y1 REF OUT PROMPT"""
import base64, io, json, os, sys, urllib.request
from PIL import Image
src, x0, y0, x1, y1, ref, out, prompt = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6], sys.argv[7], sys.argv[8]
page = Image.open(src).convert("RGB"); panel = page.crop((x0, y0, x1, y1))
def png(im): buf = io.BytesIO(); im.save(buf, "PNG"); return buf.getvalue()
b = "----p211r"
parts = [("model", "gpt-image-2"), ("prompt", prompt), ("size", "1536x1024"), ("quality", "high")]
body = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in parts)
for name, data in (("panel.png", png(panel.resize((1536, 1024), Image.LANCZOS))), ("ref.png", open(ref, "rb").read())):
    body += f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="{name}"\r\nContent-Type: image/png\r\n\r\n'.encode() + data + b"\r\n"
body += f"--{b}--\r\n".encode()
req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, method="POST",
                             headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": f"multipart/form-data; boundary={b}"})
try:
    with urllib.request.urlopen(req, timeout=580) as r:
        data = json.load(r)["data"][0]["b64_json"]
except urllib.error.HTTPError as e:
    sys.exit(f"{out}: HTTP {e.code} {e.read().decode()[:500]}")
new = Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB").resize(panel.size, Image.LANCZOS)
page.paste(new, (x0, y0)); page.save(out); print(out)
