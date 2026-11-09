"""hq#205: show the publish date and time under each post title (home, archive, single)."""
import json, subprocess, urllib.request
TOK = subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"], capture_output=True, text=True, check=True).stdout.strip()
H = {"Authorization": f"Bearer {TOK}", "Content-Type": "application/json"}
BASE = "https://public-api.wordpress.com/wp/v2/sites/258340798/templates/pub/assembler//"
FMT = r"F j, Y \a\t g:i a"
LIST = '<!-- wp:post-title {"isLink":true,"className":"no-underline","fontSize":"medium"} /-->'
SINGLE = '<!-- wp:post-title {"textAlign":"center","fontSize":"large"} /-->'
for slug, anchor, attrs in (("home", LIST, {}), ("archive", LIST, {}), ("single", SINGLE, {"textAlign": "center"})):
    t = json.load(urllib.request.urlopen(urllib.request.Request(BASE + slug + "?context=edit", headers=H), timeout=60))
    raw = t["content"]["raw"]
    if "wp:post-date" in raw: continue
    assert raw.count(anchor) == 1, slug
    block = f'<!-- wp:post-date {json.dumps({**attrs, "format": FMT, "fontSize": "small"})} /-->'
    raw = raw.replace(anchor, anchor + "\n\n" + block)
    r = json.load(urllib.request.urlopen(urllib.request.Request(BASE + slug, data=json.dumps({"content": raw}).encode(), headers=H, method="POST"), timeout=60))
    print("updated", r["id"], r["source"])
