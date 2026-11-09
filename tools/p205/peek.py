import json, subprocess, urllib.request, sys
TOK = subprocess.run(["security","find-generic-password","-s","wpcom_token","-w"],capture_output=True,text=True,check=True).stdout.strip()
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": f"Bearer {TOK}"}), timeout=60) as r: return json.load(r)
for t in get("https://public-api.wordpress.com/wp/v2/sites/258340798/templates?context=edit"):
    if t.get("source") == "custom" or t["slug"] in ("home","index","archive"):
        print("=== TEMPLATE", t["id"], t["source"]); print(t["content"]["raw"][:3000])
p = get("https://public-api.wordpress.com/rest/v1.1/sites/258340798/posts/25?context=edit")
print("=== 25", p["status"], p["content"][-400:])
print(get("https://public-api.wordpress.com/rest/v1.1/sites/578271/posts/1308?context=edit&fields=ID,status,title,content")["content"][:600])
