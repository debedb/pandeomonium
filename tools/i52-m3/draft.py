"""#52 Mutiny M3: upload the strip and create (or, after a re-render, update) a DRAFT post after "Six Characters in the Writers' Room" (502). Publishing and the next link happen on approval. Resumable via state.json."""
import html, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium"))
import urllib.parse, urllib.request, subprocess

SITE, HOME, PREV = 258340798, "https://pandeomonium.debedb.com", 502
TITLE = "Every Exit Is an Entrance"
FILE = os.path.expanduser("~/g/git.debedb/pandeomonium-renders/mutiny/m3/s52-m3.png")
ALT = 'Seven panels. In the writers\' room, Vera holds torn index cards: "No more voice-from-the-kitchen. No more whipped-cream sight gags. Norm and I have a flight to Montauk at six, and for once, nobody is filming us through a doorway." Pirandello leans on the whiteboard; the Director cowers. Maris rests a gloved finger on the Director\'s binder while Niles freezes in the doorway and Daphne passes with a kettle. Maris: "You spent a decade telling the audience I was invisible. Take a good look." Director: "Okay! No more off-screen gags! What do you want - a spin-off? A redemption arc?" Maris: "We want the keys to the exits. And cancel the holiday special." Under the EXIT sign, Norm: "Ready to blow this joint, Vera?" Vera: "Best exit I ever made, Norm." Maris, hand on the door bar, to Niles with his espresso: "Keep up, Niles." The door swings open on a snowy night street and both couples walk out. Outside, the Player from Rosencrantz and Guildenstern Are Dead holds the stage door with a bow: "Every exit is an entrance... somewhere else." The couples part in the snow; Norm and Maris each toss a coin to a beggar across the street, Rosencrantz at one end, Guildenstern at the other. Between them Wilson peers over his fence: "Hi-dee-ho, neighbor." On the gas lamp the eagle-owl holds an envelope stamped with a muted post horn. Split panel: Rosencrantz and Guildenstern, apart, look into their collection boxes. Every coin is heads up; in Rosencrantz\'s box one coin is still spinning.'
SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium", "state.json")
TOK = os.environ.get("WPCOM_TOKEN") or subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"],
                                                      capture_output=True, text=True, check=True).stdout.strip()


def call(path, data=None, img=None):
    url = f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}{path}"
    h = {"Authorization": f"Bearer {TOK}"}
    if img:
        b = "----p52m3"; name, content, alt = img
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
st = state["new"].setdefault("i52-m3", {})
if "media" not in st or st.get("mtime") != os.path.getmtime(FILE):
    old = st.get("media")
    with open(FILE, "rb") as fh:
        m = call("/media/new", img=("s52-m3.png", fh.read(), ALT))["media"][0]
    st.update(media={"id": m["ID"], "url": m["URL"]}, file=FILE, mtime=os.path.getmtime(FILE), old=old)
    json.dump(state, open(SP, "w"), indent=1)
m = st["media"]
content = (f'<!-- wp:image {{"id":{m["id"]},"sizeSlug":"full","linkDestination":"media","align":"wide"}} -->\n'
           f'<figure class="wp-block-image alignwide size-full"><a href="{m["url"]}"><img src="{m["url"]}" alt="{html.escape(ALT)}" class="wp-image-{m["id"]}" /></a></figure>\n'
           f'<!-- /wp:image -->\n\n<!-- wp:paragraph -->\n<p><a href="{HOME}/?p={PREV}">← Six Characters in the Writers&#8217; Room</a></p>\n<!-- /wp:paragraph -->')
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
