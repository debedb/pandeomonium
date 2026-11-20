# #34: seven panels in parallel, each with its likeness references; retries on transient errors. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd); R=$HOME/g/git.debedb/pandeomonium-renders/perl/refs
cd ~/g/git.debedb/pandeomonium-renders/perl
refs(){ case $1 in
  1) echo $R/wall.png $R/wall2.png;;
  2) echo $R/c8_410.png $R/c5_410.png;;
  3) echo $R/c8_410.png $R/gross.png;;
  4) echo $R/oreilly_ie.png $R/oreilly_ie2.png $R/chomsky_strip.png $R/chomsky_strip2.png $R/eco_strip.png;;
  5) echo $R/c3_410.png;;
  6) echo $R/oreilly_ie.png $R/oreilly_ie2.png $R/chomsky_strip.png $R/eco_strip.png;;
  7) echo $R/sting_strip.png;;
esac; }
for i in ${@:-1 2 3 4 5 6 7}; do
  cat $P/style.txt $P/p$i.txt > pr-$i.txt
  (for k in 1 2 3; do SIZE=1536x1024 python3 $G pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6 7}; do echo "c$i: $(head -c 200 g$i.log)"; done
