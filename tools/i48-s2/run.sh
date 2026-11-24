# #48 strip 2 The Transaction: eight panels in parallel. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd)
mkdir -p ~/g/git.debedb/pandeomonium-renders/orchard/s2; cd ~/g/git.debedb/pandeomonium-renders/orchard/s2; R=../refs
refs(){ case $1 in
  1|2) echo $R/c-lopakhin.png $R/c-ranevskaya.png $R/c-varya.png $R/varya.png $R/levene.png;;
  3) echo $R/c-lopakhin.png $R/c-varya.png $R/varya.png $R/c-ranevskaya.png $R/levene.png;;
  4|5|6) echo $R/c-lopakhin.png $R/c-varya.png $R/varya.png;;
  7) echo $R/c-lopakhin.png $R/c-varya.png $R/varya.png $R/levene.png;;
  8) echo $R/c-varya.png $R/varya.png;;
esac; }
for i in ${@:-1 2 3 4 5 6 7 8}; do
  python3 - "$P" $i > pr-$i.txt <<'PY'
import sys
P, i = sys.argv[1], sys.argv[2]
cast = dict(l.split("=", 1) for l in open(f"{P}/cast.txt").read().splitlines() if l)
t = open(f"{P}/style.txt").read() + open(f"{P}/p{i}.txt").read()
for k, v in cast.items():
    t = t.replace(k, v, 1).replace(k, v.split(" (")[0])
print(t)
PY
  (for k in 1 2 3; do SIZE=1536x1024 python3 $G pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6 7 8}; do echo "c$i: $(head -c 200 g$i.log)"; done
