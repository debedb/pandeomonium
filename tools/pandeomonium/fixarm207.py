"""hq#207 strip 1, panel 4: redraw the worker so the right hand holds the phone and the left hand holds the menu."""
import base64, io, json, os, sys, urllib.request
from PIL import Image
D = sys.argv[1]
BOX = (10, 494, 512, 1014)
src = Image.open(os.path.join(D, "s1.png")).convert("RGB")
panel = src.crop(BOX)
buf = io.BytesIO(); panel.resize((1024, 1024), Image.LANCZOS).save(buf, "PNG")
PROMPT = ("Redraw this comic panel in exactly the same art style, colors, background, lighting, framing and speech bubble. "
          "Fix the man's arms: he is seen from behind. His RIGHT arm (on the right side of the image) is raised with the elbow out, "
          "and his right hand holds the black telephone handset to his right ear. His LEFT arm (on the left side of the image) holds "
          "the paper menu up in front of him so it is visible past his left shoulder; the menu still reads, one item per line: "
          "40 宫保鸡丁 / 41 麻婆豆腐 / 43 糖醋里脊 / 44 鱼香茄子. Each hand clearly belongs to its own arm. Keep the red shirt, hair, stacked plates and the 福 sign.")
b = "----p207"
body = b"".join([
    f'--{b}\r\nContent-Disposition: form-data; name="model"\r\n\r\ngpt-image-2\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="prompt"\r\n\r\n{PROMPT}\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="size"\r\n\r\n1024x1024\r\n'.encode(),
    f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="p.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + buf.getvalue() + b"\r\n",
    f"--{b}--\r\n".encode()])
req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, method="POST",
                             headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": f"multipart/form-data; boundary={b}"})
with urllib.request.urlopen(req, timeout=300) as r:
    out = json.load(r)
new = Image.open(io.BytesIO(base64.b64decode(out["data"][0]["b64_json"]))).convert("RGB").resize(panel.size, Image.LANCZOS)
n = len([f for f in os.listdir(D) if f.startswith("p4-try")])
new.save(os.path.join(D, f"p4-try{n}.png")); print(f"p4-try{n}.png")
