"""hq#212: swap the strip image on an already published post in place, keeping its status and its nav links.
Usage: update212.py KEY IMAGE ALT"""
import json, os, sys
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish210.py")).read()
exec(src[:src.index("S = [")])  # shared call/para/figure helpers and state, stops before publish210's work

key, image, alt = sys.argv[1:4]
st = state["new"][key]
with open(image, "rb") as fh:
    m = call(NEW, "/media/new", img=(os.path.basename(image), fh.read(), alt, st["id"]))["media"][0]
st.update(media={"id": m["ID"], "url": m["URL"]}, file=os.path.abspath(image), mtime=os.path.getmtime(image))
json.dump(state, open(SP, "w"), indent=1)
live = call(NEW, f'/posts/{st["id"]}?context=edit')
i = live["content"].index("<!-- wp:paragraph")
r = call(NEW, f'/posts/{st["id"]}', {"content": figure(st["media"], alt) + "\n\n" + live["content"][i:]})
print(st["id"], r["status"], r["URL"])
