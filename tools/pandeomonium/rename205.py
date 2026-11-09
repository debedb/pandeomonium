"""hq#205: retitle 55 and 58, fix the nav link text that names them, keep state/publish205 in sync."""
import json, os, re, subprocess, urllib.parse, urllib.request
TOK = subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"], capture_output=True, text=True, check=True).stdout.strip()
def call(path, data=None):
    req = urllib.request.Request(f"https://public-api.wordpress.com/rest/v1.1/sites/258340798{path}", headers={"Authorization": f"Bearer {TOK}"},
                                 data=urllib.parse.urlencode(data).encode() if data else None, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=90) as r: return json.load(r)
R = {"Update My Prior": ("The Tale of Two Thomases", "the-tale-of-two-thomases", 55), "Superposition": ("Six More Weeks...", "six-more-weeks", 58)}
for old, (new, slug, pid) in R.items():
    r = call(f"/posts/{pid}", {"title": new, "slug": slug}); print(pid, r["status"], r["title"], r["URL"])
for pid in (25, 55, 58):
    c = call(f"/posts/{pid}?context=edit")["content"]; n = c
    for old, (new, _, _) in R.items(): n = n.replace(f"← {old}<", f"← {new}<").replace(f">{old} →", f">{new} →")
    if n != c: call(f"/posts/{pid}", {"content": n}); print("nav", pid)
D = os.path.dirname(os.path.abspath(__file__)); SP = os.path.join(D, "state.json")
st = json.load(open(SP))
for old, (new, _, _) in R.items():
    if old in st["new"]: st["new"][new] = st["new"].pop(old)
json.dump(st, open(SP, "w"), indent=1)
p = os.path.join(D, "publish205.py"); s = open(p).read()
for old, (new, _, _) in R.items(): s = s.replace(f'"{old}"', f'"{new}"')
open(p, "w").write(s)
