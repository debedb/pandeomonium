"""hq#199: move Pandeomonium to its own site. Resumable via state.json."""
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

INTRO = ('<a href="https://en.wikipedia.org/wiki/Pandaemonium_(Paradise_Lost)">Pandeomonium</a> is a comic series without an end, in which prophets, saints and philosophers share one road, one Uber and one garage. '
         'It keeps to its own continuity, not to the calendar: that the Buddha gives the Magi directions five centuries late is the joke, not the mistake. With a tip of the hat to <a href="https://en.wikipedia.org/wiki/Dilbert">Scott Adams</a>.')
CREDIT = "Samurai contributed by a friend of the series."
ONWARD = f'Pandeomonium continues at <a href="{HOME}/">pandeomonium.debedb.com</a>.'
S = [  # file, title, date, slug-key, alt, lead text
 ("strip-1.png", "Right of Way", "2026-10-22T12:00:00-07:00", "Three panels. Jesus walks on the sea, smiling. Moses, on a cliff, raises his staff and the sea parts beneath Jesus, who drops. Jesus sits in the dry seabed between walls of water, shaking his fist at Moses.", INTRO),
 ("strip-2.png", "Upgrade", "2026-10-23T07:45:00-07:00", "Three panels. Moses strikes a rock and water pours into a basin; people drink. Jesus touches the stream and it turns to wine. Everyone sprawls drunk and laughing around Jesus while Moses glares.", None),
 ("strip-3.png", "Directions", "2026-10-23T15:45:00-07:00", "Four panels. The three Magi follow the star with their gifts. Clouds hide the star and they look lost. Under a tree they ask the meditating Buddha: \"Which path leads to Bethlehem?\" The Buddha answers: \"The path is eightfold.\"", None),
 ("guest-samurai-strip.png", "Forking Paths", "2026-10-23T18:00:00-07:00", "Five panels. The three Magi follow the star, lose it, and ask the Buddha: \"Which path leads to Bethlehem?\" The Buddha answers: \"The path is eightfold.\" In the last panel a samurai seated beside the Buddha says in Japanese: \"A samurai has no goal, only the Way.\" Jorge Luis Borges, standing nearby with a cane, thinks: \"Is this the garden of forking paths?\"", CREDIT),
 ("strip-4.png", "Ride Confirmed", "2026-10-24T12:00:00-07:00", "Two panels. One of the Magi, phone in hand, says \"I'll call an uber\" as the Buddha meditates beside them. Close-up of the phone: \"Your ride is confirmed. Your driver is Mohammed.\"", None),
 ("strip-5.png", "Roadside Assistance", "2026-10-25T12:00:00-07:00", "Four panels. The Uber has broken down, hood up and steaming, its driver holding his head. Jesus arrives standing on the cross-shaped boom of a tow truck. He hops down, hooks up the car, and tows it away with the Magi waving from inside.", None),
 ("strip-6.png", "Works on My Machine", "2026-10-26T12:00:00-07:00", "Three panels. The tow truck delivers the Uber and the Magi to a village garage, where the mechanic, Tertullian, waits. The driver, Mohammed, pleads: \"But it was working, don't you believe me?\" Tertullian, head under the hood, answers: \"credo quia absurdum\".", None),
 ("strip-bacon.png", "Either One of Them", "2026-10-27T12:00:00-07:00", "Four panels. Tertullian, wrench in hand: \"I cannot figure out what's wrong here. I need to consult a colleague.\" He dials a phone. Holding the receiver out to Mohammed: \"I don't know, either one of them, Roger or Francis...\" Mohammed, on the phone: \"Bacon?\"", None),
 ("strip-car-talk.png", "Don't Drive Like My Brother", "2026-10-28T12:00:00-07:00", "Three panels in a radio studio, on air. A friar and an Elizabethan gentleman in a ruff, both in headphones: \"Hello, you're on Car Talk!\" Two laughing radio hosts: \"Don't drive like my brother!\" \"And don't drive like MY brother!\"", None),
 ("strip-ockham.png", "Extra Parts", "2026-10-29T12:00:00-07:00", "Three panels. A radio host: \"We have someone on the other line calling just now saying he knows what the problem is.\" A tonsured friar, William of Ockham, shaves with a straight razor at a basin while holding a telephone. Close-up, razor at his cheek: \"Someone added extra parts to that engine\".", None),
 ("doc-part-121g-final.png", "Part 121g", "2026-10-30T12:00:00-07:00", "Four panels. Tertullian yells: \"Hey, Doc!\" Doc Brown appears in a lab coat and yellow suit, goggles on his forehead; Tertullian points at the engine: \"WTF IS THAT?\" Doc sheepishly holds up the glowing Y-shaped device he has pulled out. An office manager with an invoice asks Tertullian: \"Hey boss, what is this charge for part 121g from O'Reilly?\"", None),
]

def para(t): return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"
def figure(m, alt):
    return (f'<!-- wp:image {{"id":{m["id"]},"sizeSlug":"full","linkDestination":"media"}} -->\n'
            f'<figure class="wp-block-image size-full"><a href="{m["url"]}"><img src="{m["url"]}" alt="{html.escape(alt)}" class="wp-image-{m["id"]}"/></a></figure>\n<!-- /wp:image -->')

print(call(NEW, "/settings", {"blogname": "Pandeomonium", "blogdescription": "A comic series without an end"}).get("updated"))
try: call(NEW, "/posts/3/delete", {})
except Exception as e: print("hello world:", e)

# reserve drafts + upload images
for f, title, date, alt, lead in S:
    if title in state["new"]: continue
    p = call(NEW, "/posts/new", {"title": title, "status": "draft", "date": date, "tags": "comics"})
    with open(os.path.join(D, f), "rb") as fh:
        m = call(NEW, "/media/new", img=(f, fh.read(), alt, p["ID"]))["media"][0]
    state["new"][title] = {"id": p["ID"], "media": {"id": m["ID"], "url": m["URL"]}}
    json.dump(state, open(SP, "w"), indent=1)

# fill + publish, oldest first
for i, (f, title, date, alt, lead) in enumerate(S):
    st = state["new"][title]
    if st.get("done"): continue
    nav = []
    if i > 0: nav.append(f'<a href="{HOME}/?p={state["new"][S[i-1][1]]["id"]}">← {html.escape(S[i-1][1])}</a>')
    if i < len(S) - 1: nav.append(f'<a href="{HOME}/?p={state["new"][S[i+1][1]]["id"]}">{html.escape(S[i+1][1])} →</a>')
    parts = ([para(lead)] if lead else []) + [figure(st["media"], alt), para(" · ".join(nav))]
    r = call(NEW, f'/posts/{st["id"]}', {"content": "\n\n".join(parts), "featured_image": st["media"]["id"], "status": "publish", "date": date})
    assert r["status"] == "publish", title
    st["done"] = True; st["url"] = r["URL"]; json.dump(state, open(SP, "w"), indent=1)
    print(st["id"], title, r["date"][:10], r["URL"])

# blog: the transitional strip
g = next(x for x in S if x[1] == "Forking Paths")
if not state["blog_guest"]:
    with open(os.path.join(D, g[0]), "rb") as fh:
        m = call(BLOG, "/media/new", img=("comic-forking-paths.png", fh.read(), g[3], 0))["media"][0]
    body = [figure({"id": m["ID"], "url": m["URL"]}, g[3]), para(CREDIT + " " + ONWARD), para('<a href="https://blog.debedb.com/?p=1304">← Directions</a>')]
    r = call(BLOG, "/posts/new", {"title": g[1], "status": "publish", "date": "2026-10-23T18:00:00-07:00", "categories": "pandeomonium", "tags": "comics", "content": "\n\n".join(body), "featured_image": m["ID"]})
    assert r["status"] == "publish"
    state["blog_guest"] = r["ID"]; json.dump(state, open(SP, "w"), indent=1)
    print("blog", r["ID"], r["URL"], list(r["categories"]))

# blog: pointers on the three published strips, next link on Directions
gid = state["blog_guest"]
for pid in (1302, 1303, 1304):
    live = call(BLOG, f"/posts/{pid}?context=edit")["content"]
    if "pandeomonium.debedb.com/" in live: continue
    new = live.rstrip()
    if pid == 1304:
        old = '<a href="https://blog.debedb.com/?p=1303">← Upgrade</a></p>'
        assert new.count(old) == 1
        new = new.replace(old, f'<a href="https://blog.debedb.com/?p=1303">← Upgrade</a> · <a href="https://blog.debedb.com/?p={gid}">Forking Paths →</a></p>')
    new += "\n\n" + para(ONWARD)
    r = call(BLOG, f"/posts/{pid}", {"content": new})
    assert r["status"] == "publish"; print("pointer", pid)

# blog: retire the drafts now live on the new site (trash, recoverable); 1308 stays for its own issue
for pid in (1305, 1306, 1307):
    p = call(BLOG, f"/posts/{pid}?context=edit")
    if p["status"] == "draft":
        call(BLOG, f"/posts/{pid}/delete", {}); print("trashed", pid)
