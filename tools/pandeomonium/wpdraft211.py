"""hq#211: create or refresh one strip as a WordPress draft, nav-linked to the previous post. Never publishes.
Usage: wpdraft211.py KEY IMAGE TITLE ALT PREV_KEY PREV_TITLE"""
import json, os, sys
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish210.py")).read()
exec(src[:src.index("S = [")])  # shared call/para/figure helpers and state, stops before publish210's work

key, image, title, alt, prev_key, prev_title = sys.argv[1:7]
st = state["new"].get(key)
if not st:
    p = call(NEW, "/posts/new", {"title": title, "status": "draft", "tags": "comics"})
    st = state["new"][key] = {"id": p["ID"]}
    json.dump(state, open(SP, "w"), indent=1)
if st.get("file") != os.path.abspath(image) or st.get("mtime") != os.path.getmtime(image):
    with open(image, "rb") as fh:
        m = call(NEW, "/media/new", img=(os.path.basename(image), fh.read(), alt, st["id"]))["media"][0]
    st.update(media={"id": m["ID"], "url": m["URL"]}, file=os.path.abspath(image), mtime=os.path.getmtime(image))
    json.dump(state, open(SP, "w"), indent=1)
nav = para(f'<a href="{HOME}/?p={state["new"][prev_key]["id"]}">← {html.escape(prev_title)}</a>')
r = call(NEW, f'/posts/{st["id"]}', {"title": title, "content": "\n\n".join([figure(st["media"], alt), nav]), "featured_image": "", "status": "draft"})
assert r["status"] == "draft", r["status"]
print(st["id"], r["status"], f'https://wordpress.com/post/pandeomonium.debedb.com/{st["id"]}', f'{HOME}/?p={st["id"]}&preview=true')
