"""#27: publish «Allen key цветочек» after The Watch (391) and add the next link to The Watch. Resumable via state.json."""
import html, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium"))
import urllib.parse, urllib.request, subprocess

SITE, HOME, PREV = 258340798, "https://pandeomonium.debedb.com", 391
TITLE = "Allen key цветочек"
FILE = os.path.expanduser("~/g/git.debedb/pandeomonium-renders/ikea/s27.png")
ALT = ("In an IKEA, the Minotaur in a staff vest studies the store map, which is a labyrinth. In the cafeteria Karlsson eats meatballs, "
       "Holmes drinks tea and the python looks on, while a fighter plane flies past the window. Dedushkin runs down a warehouse aisle "
       "with Inspector Tikhonov after him on a motorcycle. Stradivari assembles a violin from flat-pack instructions while Amati watches. "
       "Dedushkin packs the violin into a case. At the checkout Caroline Campbell and HAUSER play violin and cello as two Tikhonovs "
       "lead two handcuffed Dedushkins away.")
SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium", "state.json")
TOK = os.environ.get("WPCOM_TOKEN") or subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"],
                                                      capture_output=True, text=True, check=True).stdout.strip()


def call(path, data=None, img=None):
    url = f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}{path}"
    h = {"Authorization": f"Bearer {TOK}"}
    if img:
        b = "----p27"; name, content, alt = img
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
st = state["new"].setdefault("i27", {})
if "media" not in st:
    with open(FILE, "rb") as fh:
        m = call("/media/new", img=("s27.png", fh.read(), ALT))["media"][0]
    st.update(media={"id": m["ID"], "url": m["URL"]}, file=FILE, mtime=os.path.getmtime(FILE))
    json.dump(state, open(SP, "w"), indent=1)
m = st["media"]
content = (f'<!-- wp:image {{"id":{m["id"]},"sizeSlug":"full","linkDestination":"media","align":"wide"}} -->\n'
           f'<figure class="wp-block-image alignwide size-full"><a href="{m["url"]}"><img src="{m["url"]}" alt="{html.escape(ALT)}" class="wp-image-{m["id"]}" /></a></figure>\n'
           f'<!-- /wp:image -->\n\n<!-- wp:paragraph -->\n<p><a href="{HOME}/?p={PREV}">← The Watch</a></p>\n<!-- /wp:paragraph -->')
if not st.get("done"):
    r = call("/posts/new", {"title": TITLE, "status": "publish", "tags": "comics", "content": content, "featured_image": m["id"]})
    assert r["status"] == "publish", r["status"]
    st.update(id=r["ID"], done=True, url=r["URL"]); json.dump(state, open(SP, "w"), indent=1)
    print(st["id"], TITLE, r["URL"])

# next link on The Watch: read live, splice, never re-post a local copy
live = call(f"/posts/{PREV}?context=edit")["content"]
old = f'<p><a href="{HOME}/?p=376">← Eighteen</a></p>'
if f"?p={st['id']}" not in live:
    assert live.count(old) == 1, "nav paragraph on The Watch changed; splice by hand"
    new = live.replace(old, f'<p><a href="{HOME}/?p=376">← Eighteen</a> · <a href="{HOME}/?p={st["id"]}">{html.escape(TITLE)} →</a></p>')
    assert call(f"/posts/{PREV}", {"content": new})["status"] == "publish"
    print("next link added to", PREV)
