"""hq#211: revise a drawn strip in place with gpt-image-2 edits (the strip itself is the base image). Usage: edit211.py BASE OUT PROMPT_FILE"""
import base64, io, json, os, sys, urllib.request
from PIL import Image
base, out, prompt = sys.argv[1], sys.argv[2], open(sys.argv[3]).read()
b = "----p211e"
body = b"".join([
    f'--{b}\r\nContent-Disposition: form-data; name="model"\r\n\r\ngpt-image-2\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="prompt"\r\n\r\n{prompt}\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="size"\r\n\r\n1536x1024\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="quality"\r\n\r\nhigh\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="base.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + open(base, "rb").read() + b"\r\n",
    f"--{b}--\r\n".encode()])
req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, method="POST",
                             headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": f"multipart/form-data; boundary={b}"})
try:
    with urllib.request.urlopen(req, timeout=580) as r:
        data = json.load(r)["data"][0]["b64_json"]
except urllib.error.HTTPError as e:
    sys.exit(f"{out}: HTTP {e.code} {e.read().decode()[:500]}")
Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB").save(out); print(out)
