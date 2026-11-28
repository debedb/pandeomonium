# #52 Mutiny M3: panels in parallel. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd)
mkdir -p ~/g/git.debedb/pandeomonium-renders/mutiny/m3; cd ~/g/git.debedb/pandeomonium-renders/mutiny/m3; R=../refs
refs(){ case $1 in
  1) echo $R/c-vera.png $R/c-pirandello.png $R/c-director.png;;
  2) echo $R/c-maris.png $R/c-director.png $R/niles.png $R/daphne.png;;
  3) echo $R/c-vera.png $R/norm.png $R/c-maris.png $R/c-niles.png;;
  4) echo $R/c-vera.png $R/norm.png $R/c-maris.png $R/c-niles.png;;
  5) echo $R/player.png $R/c-vera.png $R/norm.png $R/c-maris.png $R/c-niles.png;;
  6) echo $R/player.png $R/c-rg.png $R/c-wilson.png $R/owl1.png $R/c-maris.png $R/norm.png;;
  7a|7b) echo $R/c-rg.png;;
esac; }
for i in ${@:-3 4 5 6 7a 7b}; do
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
for i in ${@:-3 4 5 6 7a 7b}; do echo "c$i: $(head -c 300 g$i.log)"; done
