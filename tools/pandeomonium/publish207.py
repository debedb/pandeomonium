"""hq#207: two strips (Oct 31 now, Nov 1 scheduled) + oldest-first toggle. Resumable via state.json; rerun after Nov 1 to add the forward link."""
import html, json, os, subprocess, urllib.parse, urllib.request
NEW, BLOG = 258340798, 578271
HOME = "https://pandeomonium.debedb.com"
D = os.path.dirname(os.path.abspath(__file__))
SP = os.path.join(D, "state.json")
state = json.load(open(SP)) if os.path.exists(SP) else {"new": {}, "blog_guest": None}
TOK = os.environ.get("WPCOM_TOKEN") or subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"], capture_output=True, text=True, check=True).stdout.strip()

def call(site, path, data=None, img=None):
    url = f"https://public-api.wordpress.com/rest/v1.1/sites/{site}{path}"
    h = {"Authorization": f"Bearer {TOK}"}
    if img:
        b = "----p199"; name, content, alt, parent = img
        body = (f'--{b}\r\nContent-Disposition: form-data; name="media[]"; filename="{name}"\r\nContent-Type: image/png\r\n\r\n').encode() + content + b"\r\n"
        for k, v in {"attrs[0][alt]": alt}.items():
            body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
        body += f"--{b}--\r\n".encode(); h["Content-Type"] = f"multipart/form-data; boundary={b}"
        req = urllib.request.Request(url, data=body, headers=h, method="POST")
    elif data is not None:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), headers=h, method="POST")
    else:
        req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)

def para(t): return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"
def figure(m, alt):
    return (f'<!-- wp:image {{"id":{m["id"]},"sizeSlug":"full","linkDestination":"media","align":"wide"}} -->\n'
            f'<figure class="wp-block-image alignwide size-full"><a href="{m["url"]}"><img src="{m["url"]}" alt="{html.escape(alt)}" class="wp-image-{m["id"]}"/></a></figure>\n<!-- /wp:image -->')


S = [
 ("strip-chinese-room.png", "Of all the joints, in all the towns, in all the universe...", None, "Six panels. John Searle at his desk, a paper titled THE CHINESE ROOM beside him, searches \"Chinese food near me\" and gets one result: 宇宙尽头的餐馆, the Restaurant at the End of the Universe. Its menu lists 40 宫保鸡丁, 41 麻婆豆腐, 42 关于生命、宇宙及万事万物的终极问题的答案 (the answer to the ultimate question of life, the universe and everything), 43 糖醋里脊, 44 鱼香茄子. Searle phones: \"Number 42, please.\" A waiter, phone in his right hand and a menu without 42 in his left: \"There's no 42 on this menu.\" Confucius studies the menu: \"We need a rectification of the menu.\" Three dolphins leave the restaurant: \"So long, and thanks for all the fish!\""),
 ("strip-ovens-of-akhnai.png", "But how high?", None, "Five panels. In the restaurant kitchen, Confucius calls Ovens of Akhnai: \"Hello, this is Ovens of Akhnai, can we help you?\" \"I need an oven fixed.\" Three rabbis watch an old repairman point at the ductwork: \"It's just a vent problem.\" He climbs a ladder past the restaurant's sign, 宇宙尽头的餐馆, and stands on the roof by the vent with a wrench. The three rabbis below point up: \"לֹא בַשָּׁמַיִם הִוא\" (\"It is not in heaven\")."),
]
prev = ("Six More Weeks...", state["new"]["Six More Weeks..."]["id"])
for f, title, date, alt in S:
    if title not in state["new"]:
        p = call(NEW, "/posts/new", {"title": title, "status": "draft", "date": date, "tags": "comics"})
        with open(os.path.join(D, f), "rb") as fh:
            m = call(NEW, "/media/new", img=(f, fh.read(), alt, p["ID"]))["media"][0]
        state["new"][title] = {"id": p["ID"], "media": {"id": m["ID"], "url": m["URL"]}}
        json.dump(state, open(SP, "w"), indent=1)
    st = state["new"][title]
    if not st.get("done"):
        nav = para(f'<a href="{HOME}/?p={prev[1]}">← {html.escape(prev[0])}</a>')
        r = call(NEW, f'/posts/{st["id"]}', {"content": "\n\n".join([figure(st["media"], alt), nav]), "featured_image": "", "status": "publish", "publicize_message": title, **({"date": date} if date else {})})
        assert r["status"] in ("publish", "future"), (title, r["status"])
        st["done"] = True; st["url"] = r["URL"]; json.dump(state, open(SP, "w"), indent=1)
        print(st["id"], title, r["status"], r["date"], r["URL"])
    prev = (title, st["id"])

# forward links, only once the next post is live (no live post links to a scheduled one)
order = ["Six More Weeks..."] + [s[1] for s in S]
for a, b in zip(order, order[1:]):
    pa, pb = state["new"][a]["id"], state["new"][b]["id"]
    if call(NEW, f"/posts/{pb}?fields=status")["status"] != "publish": print("not live yet:", b); continue
    live = call(NEW, f"/posts/{pa}?context=edit")["content"]
    if f"?p={pb}\"" in live: continue
    i = live.rindex("</a></p>") + len("</a>")
    new = live[:i] + f' · <a href="{HOME}/?p={pb}">{html.escape(b)} →</a>' + live[i:]
    call(NEW, f"/posts/{pa}", {"content": new}); print("next link", a, "->", b)

