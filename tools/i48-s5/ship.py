"""#48 strip 5: on approval, publish the draft and add the next link to "Weak Leads" (474). Reads both posts live."""
import html, json, os, subprocess, urllib.parse, urllib.request
SITE, HOME, PREV = 258340798, "https://pandeomonium.debedb.com", 474
SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium", "state.json")
TOK = os.environ.get("WPCOM_TOKEN") or subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"],
                                                      capture_output=True, text=True, check=True).stdout.strip()
def call(path, data=None):
    req = urllib.request.Request(f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}{path}",
                                 data=urllib.parse.urlencode(data).encode() if data else None,
                                 headers={"Authorization": f"Bearer {TOK}"}, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)
state = json.load(open(SP)); st = state["new"]["i48-5"]
post = call(f"/posts/{st['id']}?context=edit")
if post["status"] != "publish":
    r = call(f"/posts/{st['id']}", {"status": "publish"})
    assert r["status"] == "publish", r["status"]
    st["url"] = r["URL"]; json.dump(state, open(SP, "w"), indent=1)
    print("published", st["id"], post["title"], r["URL"])
live = call(f"/posts/{PREV}?context=edit")["content"]
old = f'<a href="{HOME}/?p=468">← Sokath, his eyes uncovered</a></p>'
if f"?p={st['id']}" not in live:
    assert live.count(old) == 1, "nav paragraph on 474 changed; splice by hand"
    new = live.replace(old, f'<a href="{HOME}/?p=468">← Sokath, his eyes uncovered</a> · <a href="{HOME}/?p={st["id"]}">{html.escape(post["title"])} →</a></p>')
    assert call(f"/posts/{PREV}", {"content": new})["status"] == "publish"
    print("next link added to", PREV)
