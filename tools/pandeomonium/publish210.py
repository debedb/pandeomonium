"""hq#210: two strips cut from one image, published now and chained after s208-10. Resumable via state.json."""
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
        h["Content-Type"] = "application/json"  # publicize_message was ignored when form-encoded (2026-10-31)
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=h, method="POST")
    else:
        req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)

def para(t): return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"
def figure(m, alt):
    return (f'<!-- wp:image {{"id":{m["id"]},"sizeSlug":"full","linkDestination":"media","align":"wide"}} -->\n'
            f'<figure class="wp-block-image alignwide size-full"><a href="{m["url"]}"><img src="{m["url"]}" alt="{html.escape(alt)}" class="wp-image-{m["id"]}"/></a></figure>\n<!-- /wp:image -->')


S = [
 ("s210-1.png", "Ganesha in the room", None, "Six panels. An old man takes a menu from a printer; item 42 is circled: \"关于生命、宇宙及万事万物的终极问题的答案\" (\"The answer to the ultimate question of life, the universe and everything\"). He feeds it into a slot marked \"Insert your order here\" in a red door under the sign \"中國密室 The Chinese Room\". Inside, a vast library: a blind old librarian with a cane reads the order. Homer, in a laurel wreath, and the librarian look up at a great golden statue beside a copy of La Vie mode d'emploi. The statue is Ganesha, who looks on as Milton assembles a jigsaw puzzle of Ganesha on the table."),
 ("s210-2.png", "Forget it, Jake.", None, "Four panels. Outside The Chinese Room, the old man sits on the step checking his watch. In a neon-lit Chinatown street, Jake Gittes, in a fedora with a cigarette, checks his watch too. The two sit side by side, waiting. A man in glasses puts a hand on Jake's shoulder: \"Forget it, Jake, it's Chinatown.\""),
]
prev = ("Untitled", state["new"]["s208-10.png"]["id"])
for f, title, date, alt in S:
    key = f
    if key not in state["new"]:
        p = call(NEW, "/posts/new", {"title": title, "status": "draft", "date": date, "tags": "comics"})
        with open(os.path.join(D, f), "rb") as fh:
            m = call(NEW, "/media/new", img=(f, fh.read(), alt, p["ID"]))["media"][0]
        state["new"][key] = {"id": p["ID"], "media": {"id": m["ID"], "url": m["URL"]}}
        json.dump(state, open(SP, "w"), indent=1)
    st = state["new"][key]
    if not st.get("done"):
        nav = para(f'<a href="{HOME}/?p={prev[1]}">← {html.escape(prev[0])}</a>')
        r = call(NEW, f'/posts/{st["id"]}', {"content": "\n\n".join([figure(st["media"], alt), nav]), "featured_image": "", "status": "publish", "publicize_message": title, **({"date": date} if date else {})})
        assert r["status"] in ("publish", "future"), (title, r["status"])
        st["done"] = True; st["url"] = r["URL"]; json.dump(state, open(SP, "w"), indent=1)
        print(st["id"], title, r["status"], r["date"], r["URL"])
    prev = (title, st["id"])

# forward links, only once the next post is live (no live post links to a scheduled one)
order = [("s208-10.png", "Untitled")] + [(s[0], s[1]) for s in S]
for (ka, a), (kb, b) in zip(order, order[1:]):
    pa, pb = state["new"][ka]["id"], state["new"][kb]["id"]
    if call(NEW, f"/posts/{pb}?fields=status")["status"] != "publish": print("not live yet:", b); continue
    live = call(NEW, f"/posts/{pa}?context=edit")["content"]
    if f"?p={pb}\"" in live: continue
    i = live.rindex("</a></p>") + len("</a>")
    new = live[:i] + f' · <a href="{HOME}/?p={pb}">{html.escape(b)} →</a>' + live[i:]
    call(NEW, f"/posts/{pa}", {"content": new}); print("next link", a, "->", b)

