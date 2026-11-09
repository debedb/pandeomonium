"""hq#212: draw a panel with gpt-image-2 from the given reference images only. Usage: gen212.py PROMPT_FILE OUT REF [REF...]"""
import base64, io, json, os, sys, urllib.request
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
prompt, out = open(sys.argv[1]).read(), sys.argv[2]
refs = sys.argv[3:]
b = "----p211"
body = b"".join([
    f'--{b}\r\nContent-Disposition: form-data; name="model"\r\n\r\ngpt-image-2\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="prompt"\r\n\r\n{prompt}\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="size"\r\n\r\n{os.environ.get("SIZE", "1536x1024")}\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="quality"\r\n\r\nhigh\r\n'.encode(),
    *[f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="ref{i}.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + open(r, "rb").read() + b"\r\n" for i, r in enumerate(refs)],
    f"--{b}--\r\n".encode()])
req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, method="POST",
                             headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": f"multipart/form-data; boundary={b}"})
try:
    with urllib.request.urlopen(req, timeout=580) as r:
        data = json.load(r)["data"][0]["b64_json"]
except urllib.error.HTTPError as e:
    sys.exit(f"{out}: HTTP {e.code} {e.read().decode()[:500]}")
Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB").save(out); print(out)
