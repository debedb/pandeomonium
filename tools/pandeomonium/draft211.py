"""hq#211: upload a draft strip to the Pandeomonium media library (unattached) and post it as a review comment on hq#211. Usage: draft211.py IMG CAPTION"""
import json, os, subprocess, sys, tempfile, urllib.request
NEW = 258340798
img, caption = sys.argv[1], sys.argv[2]
TOK = subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"], capture_output=True, text=True, check=True).stdout.strip()
b = "----p211"; name = os.path.basename(img)
body = (f'--{b}\r\nContent-Disposition: form-data; name="media[]"; filename="{name}"\r\nContent-Type: image/png\r\n\r\n').encode() + open(img, "rb").read() + f"\r\n--{b}--\r\n".encode()
req = urllib.request.Request(f"https://public-api.wordpress.com/rest/v1.1/sites/{NEW}/media/new", data=body, method="POST",
                             headers={"Authorization": f"Bearer {TOK}", "Content-Type": f"multipart/form-data; boundary={b}"})
m = json.load(urllib.request.urlopen(req, timeout=300))["media"][0]
with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
    f.write(f"{caption}\n\n<img width=\"1536\" alt=\"{name}\" src=\"{m['URL']}\" />\n\nDraft `{name}` (media {m['ID']}, not attached to any post).\n")
subprocess.run(["gh", "issue", "comment", "211", "--repo", "method-and-apparatus/hq", "--body-file", f.name], check=True)
