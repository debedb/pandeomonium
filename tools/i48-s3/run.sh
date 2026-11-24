# #48 strip 3 Closing Time: six panels in parallel. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd)
mkdir -p ~/g/git.debedb/pandeomonium-renders/orchard/s3; cd ~/g/git.debedb/pandeomonium-renders/orchard/s3; R=../refs
refs(){ case $1 in
  1) echo ../s2/c8.png;;
  2|4) echo $R/c-firs.png ../s2/c7.png;;
  3|6) echo $R/c-firs.png $R/dharmann.png $R/caine.png $R/hopper.png $R/bartlebooth-table.png $R/borges.png $R/milton.png;;
  5) echo $R/caine.png $R/hopper.png $R/dharmann.png $R/borges.png;;
esac; }
for i in ${@:-1 2 3 4 5 6}; do
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
for i in ${@:-1 2 3 4 5 6}; do echo "c$i: $(head -c 300 g$i.log)"; done
