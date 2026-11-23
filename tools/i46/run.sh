# #46 Put that coffee down: six panels in parallel, each with its likeness refs. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd)
cd ~/g/git.debedb/pandeomonium-renders/coffee; R=refs
refs(){ case $1 in
  1) echo $R/hopper.png;;
  2) echo $R/hopper.png $R/levene.png;;
  3) echo $R/blake.png $R/levene.png $R/hopper.png;;
  4) echo $R/hopper.png $R/levene.png $R/blake.png;;
  5) echo $R/pete.png $R/blake.png $R/hopper.png $R/levene.png;;
  6) echo $R/levene.png $R/hopper.png $R/blake.png $R/pete.png;;
esac; }
for i in ${@:-1 2 3 4 5 6}; do
  cat $P/style.txt $P/p$i.txt > pr-$i.txt
  (for k in 1 2 3; do SIZE=1536x1024 python3 $G pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6}; do echo "c$i: $(head -c 200 g$i.log)"; done
