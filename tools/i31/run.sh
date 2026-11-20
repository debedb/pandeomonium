# #31 cheese shop: eight panels in parallel, each with its likeness references; retries on transient errors. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd); R=/Users/gregory/g/git.debedb/pandeomonium-renders/cheese/refs
cd ~/g/git.debedb/pandeomonium-renders/cheese
refs(){ case $1 in
  1) echo $R/author.png;;
  2) echo $R/serling.png $R/author.png;;
  3) echo $R/gilliam_strip.png;;
  4) echo $R/palin.png $R/hopkins.png $R/cleese.png;;
  5) echo $R/palin.png $R/hopkins.png;;
  6) echo $R/hall.png $R/borges_strip_crop.png $R/cleese.png $R/hopkins.png $R/stipe.png;;
  7) echo $R/hall.png $R/borges_strip_crop.png $R/stipe.png $R/cleese.png $R/hopkins.png;;
  8) echo $R/hall.png $R/borges_strip_crop.png $R/cleese.png $R/palin.png $R/hopkins.png $R/stipe.png;;
esac; }
for i in ${@:-1 2 3 4 5 6 7 8}; do
  cat $P/style.txt $P/p$i.txt > pr-$i.txt
  (for k in 1 2 3; do SIZE=1536x1024 python3 $G pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6 7 8}; do echo "c$i: $(head -c 200 g$i.log)"; done
