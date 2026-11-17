"""#29: upload the strip and create a DRAFT post after «Allen key цветочек» (397). Publishing and the next link happen on approval. Resumable via state.json."""
import html, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium"))
import urllib.parse, urllib.request, subprocess

SITE, HOME, PREV = 258340798, "https://pandeomonium.debedb.com", 397
TITLE = "International Philosophy"
FILE = os.path.expanduser("~/g/git.debedb/pandeomonium-renders/football/s29.png")
ALT = 'In the Munich Olympic stadium Germany and Greece play an International Philosophy match. Confucius referees with an hourglass while the philosophers wander about thinking, and Erling Haaland meditates cross-legged on the German bench. Leibniz walks off and Jesus comes on as goalkeeper, pulling on gloves; caption: "A very controversial choice." Archimedes raises a finger: "Eureka!" Heraclitus flicks the ball past Hegel as Socrates runs in. Socrates dives to head it and Jesus catches it under the crossbar. On the touchline Kant holds up his pocket watch to Confucius, who holds up his hourglass, while Haaland meditates behind them.'
SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pandeomonium", "state.json")
TOK = os.environ.get("WPCOM_TOKEN") or subprocess.run(["security", "find-generic-password", "-s", "wpcom_token", "-w"],
                                                      capture_output=True, text=True, check=True).stdout.strip()


def call(path, data=None, img=None):
    url = f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}{path}"
    h = {"Authorization": f"Bearer {TOK}"}
    if img:
        b = "----p29"; name, content, alt = img
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
st = state["new"].setdefault("i29", {})
if "media" not in st:
    with open(FILE, "rb") as fh:
        m = call("/media/new", img=("s29.png", fh.read(), ALT))["media"][0]
    st.update(media={"id": m["ID"], "url": m["URL"]}, file=FILE, mtime=os.path.getmtime(FILE))
    json.dump(state, open(SP, "w"), indent=1)
m = st["media"]
content = (f'<!-- wp:image {{"id":{m["id"]},"sizeSlug":"full","linkDestination":"media","align":"wide"}} -->\n'
           f'<figure class="wp-block-image alignwide size-full"><a href="{m["url"]}"><img src="{m["url"]}" alt="{html.escape(ALT)}" class="wp-image-{m["id"]}" /></a></figure>\n'
           f'<!-- /wp:image -->\n\n<!-- wp:paragraph -->\n<p><a href="{HOME}/?p={PREV}">← Allen key цветочек</a></p>\n<!-- /wp:paragraph -->')
if not st.get("done"):
    r = call("/posts/new", {"title": TITLE, "status": "draft", "tags": "comics", "content": content, "featured_image": m["id"]})
    assert r["status"] == "draft", r["status"]
    st.update(id=r["ID"], done=True, url=r["URL"]); json.dump(state, open(SP, "w"), indent=1)
    print(st["id"], TITLE, f"{HOME}/?p={st['id']}&preview=true")

