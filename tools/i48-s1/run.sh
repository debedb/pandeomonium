# #48 strip 1 The Appointment: six panels in parallel. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd)
cd ~/g/git.debedb/pandeomonium-renders/orchard; R=refs
refs(){ case $1 in
  1) echo $R/doorway.png $R/levene.png $R/hopper.png;;
  2|3|4|6) echo $R/levene.png;;
  5) echo $R/levene.png;;
esac; }
size(){ case $1 in 1|2|3) echo 1024x1024;; *) echo 1536x1024;; esac; }
for i in ${@:-1 2 3 4 5 6}; do
  python3 - "$P" $i > pr-$i.txt <<'PY'
import sys
P, i = sys.argv[1], sys.argv[2]
cast = dict(l.split("=", 1) for l in open(f"{P}/cast.txt").read().splitlines() if l)
t = open(f"{P}/style{1 if i == chr(49) else chr(32)}.txt".replace(" ", "")).read() + open(f"{P}/p{i}.txt").read()
for k, v in cast.items():
    t = t.replace(k, v, 1).replace(k, v.split(" (")[0])
print(t)
PY
  (for k in 1 2 3; do SIZE=$(size $i) python3 $G pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6}; do echo "c$i: $(head -c 200 g$i.log)"; done
