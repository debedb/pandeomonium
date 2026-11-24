"""#52 The Cranes strip 2: upload the strip and create (or, after a re-render, update) a DRAFT post after "Here come the Cranes" (482). Publishing and the next link happen on approval. Resumable via state.json."""
import html, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium"))
import urllib.parse, urllib.request, subprocess

SITE, HOME, PREV = 258340798, "https://pandeomonium.debedb.com", 482
TITLE = "The Report"
FILE = os.path.expanduser("~/g/git.debedb/pandeomonium-renders/cranes/s2/s52-2.png")
ALT = "Six panels, in Russian, from Zhvanetsky's «В порту». Through a doorway off the bar, a little harbour office; on the desk lies the Hitchhiker's Guide, DON'T PANIC on its cover; through the window a toppled port crane and a V of migrating cranes with a gap in it. The boss, Viktor Ilchenko: «Послушайте, Кольцов, вы, конечно, были на работе, да?» Roman Kartsev, a beach towel round his neck: «Да!» «А?» «А?» «Это что такое?» «Что именно?» «Что у вас на шее?» «На моей?» «Это полотенце.» «При чём тут полотенце? Да вы знаете, что у вас сегодня случилось?» «Ещё бы.» «Вас искали раньше, до нашего разговора!» «Так „раньше“ или „до того“?» «Раньше... Нет, до того.» «Раньше до или до раньше того?» «Вот тут я не пойму: если вы спрашиваете, я буду отвечать. Если вы отвечаете, я буду спрашивать.» «Пока я начальник, я спрашиваю!» «Почему „пока“?» «Да вы знаете, что случилось на вашем участке или нет?» Kartsev clutches his head, staring at the window: «Стоп! Осторожно, у меня что-то с головой. Это порт?» «Порт.»"
SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium", "state.json")
TOK = os.environ.get("WPCOM_TOKEN") or subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"],
                                                      capture_output=True, text=True, check=True).stdout.strip()


def call(path, data=None, img=None):
    url = f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}{path}"
    h = {"Authorization": f"Bearer {TOK}"}
    if img:
        b = "----p52b"; name, content, alt = img
        body = (f'--{b}\r\nContent-Disposition: form-data; name="media[]"; filename="{name}"\r\nContent-Type: image/png\r\n\r\n').encode() + content + b"\r\n"
        body += f'--{b}\r\nContent-Disposition: form-data; name="attrs[0][alt]"\r\n\r\n{alt}\r\n'.encode() + f"--{b}--\r\n".encode()
        h["Content-Type"] = f"multipart/form-data; boundary={b}"
        req = urllib.request.Request(url, data=body, headers=h, method="POST")
    elif data is not None:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), headers=h, method="POST")
    else:
        req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


state = json.load(open(SP))
st = state["new"].setdefault("i52-2", {})
if "media" not in st or st.get("mtime") != os.path.getmtime(FILE):
    old = st.get("media")
    with open(FILE, "rb") as fh:
        m = call("/media/new", img=("s52-2.png", fh.read(), ALT))["media"][0]
    st.update(media={"id": m["ID"], "url": m["URL"]}, file=FILE, mtime=os.path.getmtime(FILE), old=old)
    json.dump(state, open(SP, "w"), indent=1)
m = st["media"]
content = (f'<!-- wp:image {{"id":{m["id"]},"sizeSlug":"full","linkDestination":"media","align":"wide"}} -->\n'
           f'<figure class="wp-block-image alignwide size-full"><a href="{m["url"]}"><img src="{m["url"]}" alt="{html.escape(ALT)}" class="wp-image-{m["id"]}" /></a></figure>\n'
           f'<!-- /wp:image -->\n\n<!-- wp:paragraph -->\n<p><a href="{HOME}/?p={PREV}">← Here come the Cranes. They&#8217;re American Cranes, made in America</a></p>\n<!-- /wp:paragraph -->')
if not st.get("done"):
    r = call("/posts/new", {"title": TITLE, "status": "draft", "tags": "comics", "content": content, "featured_image": m["id"]})
    assert r["status"] == "draft", r["status"]
    st.update(id=r["ID"], done=True, url=r["URL"]); json.dump(state, open(SP, "w"), indent=1)
    print(st["id"], TITLE, f"{HOME}/?p={st['id']}&preview=true")

elif st.get("old"):
    # re-render: read the live draft, swap the image block in place, keep it a draft
    o, live = st["old"], call(f"/posts/{st['id']}?context=edit")
    assert live["status"] == "draft", live["status"]
    c = live["content"]
    i, j = c.index("<!-- wp:image"), c.index("<!-- /wp:image -->") + len("<!-- /wp:image -->")
    assert str(o["id"]) in c[i:j], "image block changed; splice by hand"
    blk = content[:content.index("<!-- /wp:image -->") + len("<!-- /wp:image -->")]
    r = call(f"/posts/{st['id']}", {"title": TITLE, "content": c[:i] + blk + c[j:], "featured_image": m["id"], "status": "draft"})
    assert r["status"] == "draft", r["status"]
    st.pop("old"); json.dump(state, open(SP, "w"), indent=1)
    print("updated draft", st["id"], f"{HOME}/?p={st['id']}&preview=true")
