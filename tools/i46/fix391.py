"""#46: upload The Watch (391) with Levene redrawn as Jack Lemmon and swap it into the live post. Reads the live post and replaces only the image block's media references."""
import json, os, subprocess, urllib.parse, urllib.request
SITE, POST = 258340798, 391
FILE = os.path.expanduser("~/g/git.debedb/pandeomonium-renders/coffee/s391-fixed.png")
TOK = os.environ.get("WPCOM_TOKEN") or subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"],
                                                      capture_output=True, text=True, check=True).stdout.strip()
def call(path, data=None, body=None, ctype=None):
    h = {"Authorization": f"Bearer {TOK}"}
    if ctype: h["Content-Type"] = ctype
    req = urllib.request.Request(f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}{path}",
                                 data=body if body is not None else (urllib.parse.urlencode(data).encode() if data else None),
                                 headers=h, method="POST" if (data or body) else "GET")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)
live = call(f"/posts/{POST}?context=edit"); c = live["content"]
old_id = live["featured_image"] or None
import re
m_old = re.search(r'wp-image-(\d+)', c); old_media = m_old.group(1)
old_url = re.search(r'<img[^>]+src="([^"]+)"', c).group(1)
alt = re.search(r'alt="([^"]*)"', c).group(1)
b = "----p391"
body = (f'--{b}\r\nContent-Disposition: form-data; name="media[]"; filename="s24-levene.png"\r\nContent-Type: image/png\r\n\r\n').encode() + open(FILE, "rb").read() + b"\r\n"
body += f'--{b}\r\nContent-Disposition: form-data; name="attrs[0][alt]"\r\n\r\n{alt}\r\n'.encode() + f"--{b}--\r\n".encode()
m = call("/media/new", body=body, ctype=f"multipart/form-data; boundary={b}")["media"][0]
new = c.replace(old_url, m["URL"]).replace(f'"id":{old_media}', f'"id":{m["ID"]}').replace(f"wp-image-{old_media}", f"wp-image-{m['ID']}")
assert new != c and old_url not in new
data = {"content": new}
if live.get("featured_image"): data["featured_image"] = m["ID"]
r = call(f"/posts/{POST}", data)
print(r["status"], "old media", old_media, "->", m["ID"], m["URL"])
