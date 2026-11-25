"""#52 Mutiny M3: on approval, publish the draft and append the next link to the nav paragraph of "Six Characters in the Writers' Room" (502). Reads both posts live."""
import html, json, os, subprocess, urllib.parse, urllib.request
SITE, HOME, PREV = 258340798, "https://pandeomonium.debedb.com", 502
SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium", "state.json")
TOK = os.environ.get("WPCOM_TOKEN") or subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"],
                                                      capture_output=True, text=True, check=True).stdout.strip()
def call(path, data=None):
    req = urllib.request.Request(f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}{path}",
                                 data=urllib.parse.urlencode(data).encode() if data else None,
                                 headers={"Authorization": f"Bearer {TOK}"}, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)
state = json.load(open(SP)); st = state["new"]["i52-m3"]
post = call(f"/posts/{st['id']}?context=edit")
if post["status"] != "publish":
    r = call(f"/posts/{st['id']}", {"status": "publish"})
    assert r["status"] == "publish", r["status"]
    st["url"] = r["URL"]; json.dump(state, open(SP, "w"), indent=1)
    print("published", st["id"], post["title"], r["URL"])
live = call(f"/posts/{PREV}?context=edit")["content"]
if f"?p={st['id']}" not in live:
    anchor = f'<a href="{HOME}/?p=498">'
    i = live.index(anchor); j = live.index("</a></p>", i) + len("</a>")
    new = live[:j] + f' · <a href="{HOME}/?p={st["id"]}">{html.escape(post["title"])} →</a>' + live[j:]
    assert call(f"/posts/{PREV}", {"content": new})["status"] == "publish"
    print("next link added to", PREV)
