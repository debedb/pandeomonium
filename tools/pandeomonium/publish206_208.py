"""hq#206 + hq#208: two strips (Oct 31 now, Nov 1 scheduled) + oldest-first toggle. Resumable via state.json; rerun after Nov 1 to add the forward link."""
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
 ("s206-1.png", "The road less traveled", None, "Five panels on a Königsberg bridge at night. Euler tips his hat to Kant: \"I already saw you crossing this bridge\". Kant points up at the starry sky, then pats a book labeled MORAL CODE in his coat: \"Everything is fine.\" Alone on the bridge, a worn-out salesman with two suitcases, Willy Loman: \"Would anyone think of me???\""),
 ("s206-2.png", "Absinthe makes the heart grow fonder", None, "Three panels. Kant and Vincent van Gogh, his ear bandaged, stand on the bridge under a swirling starry night sky. Kant, looking up: \"it's beautiful\". Van Gogh: \"What?\""),
 ("s206-3.png", "Untitled", None, "Five panels. In Königsberg, townspeople set their watches as Kant walks by. Kant drives a tram over the bridge. A man runs for the switch lever, with five people tied to one track and one to the other: \"It's 5 against 1! Pull the lever!\" Kant at the controls: \"I can't. The schedule is a categorical imperative\". The tram passes the five, tied up on a bench: \"12:00. Right on time.\" \"7 + 5 = 12. Synthetic a priori.\""),
 ("s206-4.png", "Well, that's spilled oil over the tracks", None, "Four panels. A bespectacled man in a grey suit, Berlioz, lunges for the switch lever as Annushka passes with her shopping and a bottle of sunflower oil. The bottle lies broken, oil spreading over the cobbles. He slips in the oil and falls toward the tracks as the tram comes. Woland, in a beret, beside Kant: \"I told you, professor, that time at breakfast...\""),
 ("s206-5.png", "It's just Thursday at the NYT Crossword section", None, "Five panels. Kant reads the tram timetable: \"Duty is duty.\" Mussolini on a balcony, timetable and wristwatch in hand: \"Finally, someone who runs the trains on time!\" Evita sings from the next balcony, \"Don't cry for me, Königsberg,\" as Mussolini tumbles off; below, Kant: \"12:00. Right on time.\" Under a marquee reading INEVITABLE, a man on a ladder: \"It fits if we cut the E.\" Andrew Lloyd Webber: \"It's my musical, you can't cut the E.\" A third man holding the letters A and B: \"It's already hidden in there. Ten letters, starts with I.\""),
 ("s208-1.png", "Independent trials", None, "Four panels at a desert gas station. Anton Chigurh: \"What's the most you've ever lost on a coin toss?\" He flips the coin while the frightened owner stares. Outside, their horses tied up, Rosencrantz and Guildenstern watch through the window. Far outside, Monetochka sings at her keyboard: \"я вся такая мета-мета, я такая пост-пост\" (\"I'm all so meta-meta, I'm so post-post\")."),
 ("s208-2.png", "You are that man, at the crossing", None, "Six panels. A wolf catches Chigurh's coin in its teeth and pays it to a hooded ferryman waiting by his boat with a goat and a cabbage. The ferryman rows the goat across. Alla Pugacheva, hugging the wolf on the shore, sings: \"Но нас с тобой соединить паром не в силах\" (\"But no ferry can bring the two of us together\"). The ferryman rows the wolf across; the wolf, paw on his shoulder: \"я убью тебя, лодочник!\" (\"I'll kill you, boatman!\")"),
 ("s208-3.png", "The God of the copybook headings", None, "Four panels on the shore. Jesus raises a hand to Moses, who stretches his arm over the water toward the ferryman: \"Bro, stop it\". Chuck Norris and the T-1000, in a police uniform, wag their fingers at Moses. A black 1930s car pulls up with Grace and her father from Dogville inside. Her father waves Jesus and Moses in: \"Get back in the car\"."),
 ("s208-4.png", "Consider this", None, "Nine panels. In the car, Grace: \"You're right. We should burn the town down.\" Then, shimmering in a transporter beam: \"Never mind. I'll do it. Beam me up.\" On a spaceship over Earth, Ripley: \"Nuke the entire site from orbit.\" Grace: \"It's the only way to be sure.\" An orange cat lounges by the window. In a dining room the china cabinet rattles; a family looks up, then out the window at passing jets; a cat knocks a milk jug off the cabinet; a man sits alone, head in hand."),
 ("s208-5.png", "Yee-haw!", None, "Six panels. Major Kong rides a nuclear bomb out of a bomber over Earth, waving his cowboy hat. In a Soviet command bunker a screen flashes АТАКА with a missile track; the duty officer, Stanislav Petrov, reaches for the phone. Kong rides the bomb down. The screens dissolve into static reading \"Directed by David Lynch\". Petrov, palm raised: \"Stand down! Stand down!\""),
 ("s208-6.png", "Open a channel!", None, "Eight panels in the restaurant kitchen. The rabbis and Confucius stare at an oven screen showing АТАКА and \"Directed by David Lynch\". MacGyver, in an apron, holding a rewired part: \"Sorry boss, I forgot to tell you, I had to re-rig this oven.\" A rabbi: \"Can you open a channel?\" MacGyver raises Grace, Ripley and their cat on the oven screen. The rabbi, into the microphone: \"It is not in heaven! I repeat, it is not in heaven, acknowledge!\" Grace: \"Well, I guess not\". A kitchen cat and the ship's cat press paws together through the screen."),
 ("s208-7.png", "The Briggs of Königsberg", None, "Eight panels. Petrov rubs his head at his console; the intercom crackles: \"Товарищ подполковник, здесь американский офицер!\" (\"Comrade lieutenant colonel, there's an American officer here!\"). Major Briggs, in U.S. Air Force uniform, enters with Gordon Cole and salutes; Petrov salutes back. Outside in the snow, Cole: \"Why did this happen? Do you know?\" Briggs: \"I cannot tell you.\" Cole, pointing at his hearing aid: \"SPEAK LOUDER. I CANNOT HEAR YOU.\" Under a swirling starry sky, Van Gogh, his ear bandaged: \"I can't hear either. But the sky is still beautiful.\""),
 ("s208-8.png", "I think we are onto a new civilization", None, "Eight panels. The Enterprise-D over Earth beside a swirling anomaly: \"Captain's log. Stardate -- I have no idea. We just went through some ultimately irregular time/space anomaly where no stardates make sense.\" Picard: \"We know at least we are in the solar system, watching strange developments on Earth but what date is it? Computer, just log the damn thing.\" Data feeds his cat Spot. \"We are in a position over earth but we appear to be in a different time.\" \"There are life-forms in a ship orbiting the Earth and one strangely moving ... atop a rocket?\" On the viewscreen, Major Kong rides his bomb. Picard: \"Mr. Worf, shields up! Red alert!\" Troi: \"Captain. It's all good. I sense Spot telling us it's settled. We should be out of here shortly.\" Picard: \"Mr. Data... Set no course. This is highly amusing.\""),
 ("s208-9.png", "In the beginning was the log", None, "Five panels. \"Captain, the log could not be updated...\" Picard, opening a notebook: \"Well, I'll just write it down, I still know how to...\" O'Brien: \"Captain, we have a visitor beaming right onto the bridge.\" Worf: \"We could not intercept it, sir!\" The Log Lady materializes, holding her log: \"I have your log, Captain.\""),
 ("s208-10.png", "Untitled", None, "Six panels. Euler and Kant beam onto the Enterprise bridge, where the Log Lady and Picard wait. Euler, studying his map: \"This isn't one of the bridges I counted.\" Euler, to Geordi La Forge at a console showing a graph: \"What is the connection? How does it work?\" Geordi: \"Let me give you a walk-through.\" Kant gazes at the stars through the viewport. Picard, to Kant: \"Professor, would you join me in my ready room? I believe we have much to discuss.\""),
]
prev = ("But how high?", state["new"]["But how high?"]["id"])
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
order = [("But how high?", "But how high?")] + [(s[0], s[1]) for s in S]
for (ka, a), (kb, b) in zip(order, order[1:]):
    pa, pb = state["new"][ka]["id"], state["new"][kb]["id"]
    if call(NEW, f"/posts/{pb}?fields=status")["status"] != "publish": print("not live yet:", b); continue
    live = call(NEW, f"/posts/{pa}?context=edit")["content"]
    if f"?p={pb}\"" in live: continue
    i = live.rindex("</a></p>") + len("</a>")
    new = live[:i] + f' · <a href="{HOME}/?p={pb}">{html.escape(b)} →</a>' + live[i:]
    call(NEW, f"/posts/{pa}", {"content": new}); print("next link", a, "->", b)

