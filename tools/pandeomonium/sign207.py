"""hq#207: redraw one panel via gpt-image-2 edits. Usage: sign207.py SRC x0 y0 x1 y1 WxH OUT PROMPT"""
import base64, io, json, os, sys, urllib.request
from PIL import Image
src, x0, y0, x1, y1, size, out, prompt = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6], sys.argv[7], sys.argv[8]
panel = Image.open(src).convert("RGB").crop((x0, y0, x1, y1))
w, h = map(int, size.split("x"))
buf = io.BytesIO(); panel.resize((w, h), Image.LANCZOS).save(buf, "PNG")
b = "----p207"
body = b"".join([
    f'--{b}\r\nContent-Disposition: form-data; name="model"\r\n\r\ngpt-image-2\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="prompt"\r\n\r\n{prompt}\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="size"\r\n\r\n{size}\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="p.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + buf.getvalue() + b"\r\n",
    f"--{b}--\r\n".encode()])
req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, method="POST",
                             headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": f"multipart/form-data; boundary={b}"})
try:
    with urllib.request.urlopen(req, timeout=580) as r:
        data = json.load(r)["data"][0]["b64_json"]
except urllib.error.HTTPError as e:
    sys.exit(f"{out}: HTTP {e.code} {e.read().decode()[:500]}")
Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB").resize(panel.size, Image.LANCZOS).save(out); print(out)
