# #36 ready room: eight panels in parallel, each with its likeness references; retries on transient errors. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd); R=$HOME/g/git.debedb/pandeomonium-renders/enterprise/refs
cd ~/g/git.debedb/pandeomonium-renders/enterprise
refs(){ case $1 in
  1) echo $R/kant.png $R/bridge.png;;
  2) echo $R/picard.png $R/kant.png $R/bridge.png;;
  3) echo $R/joshua75.png $R/joshua249.png $R/kant.png $R/picard.png;;
  4) echo $R/spot.png $R/bridge.png;;
  5) echo $R/picard.png $R/joshua249.png $R/joshua75.png $R/kant.png;;
  6) echo $R/wesley.png $R/picard.png $R/bridge.png;;
  7) echo $R/q.png $R/wesley.png $R/picard.png;;
  8) echo $R/picard.png $R/wesley.png $R/spot.png;;
esac; }
for i in ${@:-1 2 3 4 5 6 7 8}; do
  cat $P/style.txt $P/p$i.txt > pr-$i.txt
  (for k in 1 2 3; do SIZE=1536x1024 python3 $G pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6 7 8}; do echo "c$i: $(head -c 200 g$i.log)"; done
