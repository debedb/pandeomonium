"""hq#211: publish one reviewed draft as-is, then add the forward link on the previous post.
Usage: publish211.py KEY PREV_KEY PREV_TITLE TITLE"""
import json, os, sys
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish210.py")).read()
exec(src[:src.index("S = [")])  # shared call/para/figure helpers and state, stops before publish210's work

key, prev_key, prev_title, title = sys.argv[1:5]
st, pv = state["new"][key], state["new"][prev_key]
if not st.get("done"):
    r = call(NEW, f'/posts/{st["id"]}', {"status": "publish", "publicize_message": title})
    assert r["status"] == "publish", r["status"]
    st["done"] = True; st["url"] = r["URL"]; json.dump(state, open(SP, "w"), indent=1)
    print(st["id"], r["title"], r["status"], r["date"], r["URL"])
live = call(NEW, f'/posts/{pv["id"]}?context=edit')["content"]
if f'?p={st["id"]}"' not in live:
    i = live.rindex("</a></p>") + len("</a>")
    call(NEW, f'/posts/{pv["id"]}', {"content": live[:i] + f' · <a href="{HOME}/?p={st["id"]}">{html.escape(title)} →</a>' + live[i:]})
    print("next link", prev_title, "->", title)
