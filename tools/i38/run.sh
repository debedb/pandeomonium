# #38 Ten Forward: eight panels in parallel, each with its likeness references; retries on transient errors. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd); R=$HOME/g/git.debedb/pandeomonium-renders/enterprise/tf/refs; C=$HOME/g/git.debedb/pandeomonium-renders/enterprise/refs
cd ~/g/git.debedb/pandeomonium-renders/enterprise/tf
refs(){ case $1 in
  1) echo $C/picard.png $C/joshua249.png $C/kant.png;;
  2) echo $R/guinan.png $C/q.png;;
  3) echo $C/picard.png $C/joshua249.png $C/kant.png;;
  4) echo $R/guinan.png $C/picard.png $C/joshua249.png $C/kant.png;;
  5) echo $C/picard.png $C/q.png $C/joshua249.png $C/kant.png;;
  6) echo $R/sinatra.png $R/riker.png $R/sheridan.png $R/ivanova.png;;
  7) echo $R/sinatra.png $R/riker.png;;
  8) echo $C/picard.png $C/q.png $C/joshua249.png $C/kant.png;;
esac; }
for i in ${@:-1 2 3 4 5 6 7 8}; do
  cat $P/style.txt $P/p$i.txt > pr-$i.txt
  (for k in 1 2 3; do SIZE=1536x1024 python3 $G pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6 7 8}; do echo "c$i: $(head -c 200 g$i.log)"; done
