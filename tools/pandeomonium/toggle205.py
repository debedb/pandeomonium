"""hq#205: add a newest-first / from-the-beginning toggle above the homepage query (?order=asc on the inherited main query)."""
import json, subprocess, urllib.request
TOK = subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"], capture_output=True, text=True, check=True).stdout.strip()
URL = "https://public-api.wordpress.com/wp/v2/sites/258340798/templates/pub/assembler//home"
H = {"Authorization": f"Bearer {TOK}", "Content-Type": "application/json"}
t = json.load(urllib.request.urlopen(urllib.request.Request(URL + "?context=edit", headers=H), timeout=60))
raw = t["content"]["raw"]
if "?order=asc" not in raw:
    toggle = ('<!-- wp:paragraph {"align":"center","fontSize":"small"} -->\n'
              '<p class="has-text-align-center has-small-font-size"><a href="/">Newest first</a> · <a href="/?order=asc">From the beginning</a></p>\n'
              '<!-- /wp:paragraph -->\n\n')
    anchor = '<!-- wp:query {"queryId":0'
    assert raw.count(anchor) == 1
    raw = raw.replace(anchor, toggle + anchor)
    r = json.load(urllib.request.urlopen(urllib.request.Request(URL, data=json.dumps({"content": raw}).encode(), headers=H, method="POST"), timeout=60))
    print("updated", r["id"])
