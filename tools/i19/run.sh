# #19 Data, Lore, and Mandela: seven panels in parallel, each with its likeness refs. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd)
cd ~/g/git.debedb/pandeomonium-renders/mandela; R=refs
refs(){ case $1 in
  1) echo $R/cafe.png $R/vincent.png $R/sam_deniro.png;;
  2) echo $R/cafe.png $R/data.png $R/lore.png $R/sam_deniro.png $R/vincent.png;;
  3) echo $R/cafe.png $R/lore.png $R/data.png $R/mandela.png;;
  4) echo $R/cafe.png $R/data.png $R/lore.png $R/mandela.png;;
  5) echo $R/cafe.png $R/sam_deniro.png $R/vincent.png $R/data.png $R/lore.png;;
  6) echo $R/cafe.png $R/mandela.png;;
  7) echo $R/cafe.png $R/dooley.png $R/mandela.png $R/data.png $R/sam_deniro.png;;
esac; }
size(){ [ $1 = 7 ] && echo 1536x1024 || echo 1024x1024; }
for i in ${@:-1 2 3 4 5 6 7}; do
  cat $P/style.txt $P/p$i.txt > pr-$i.txt
  (for k in 1 2 3; do SIZE=$(size $i) python3 $G pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6 7}; do echo "c$i: $(head -c 200 g$i.log)"; done
