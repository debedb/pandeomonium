# #29 philosophers' football: seven panels in parallel with established likenesses as references; retries on transient errors.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd); R=/Users/gregory/g/git.debedb/pandeomonium-renders/football/refs
cd ~/g/git.debedb/pandeomonium-renders/football
refs(){ case $1 in
  1) echo $R/confucius.png $R/confucius2.png $R/haaland.png;;
  2) echo $R/jesus.png $R/jesus2.png;;
  3) echo $R/maradona.png $R/confucius.png;;
  4) echo $R/confucius.png;;
  5) echo $R/maradona.png $R/confucius.png;;
  6) echo $R/jesus.png $R/jesus2.png $R/maradona.png;;
  7) echo $R/kant.png $R/kant_watch.png $R/confucius.png $R/haaland.png;;
esac; }
for i in ${@:-1 2 3 4 5 6 7}; do
  (for k in 1 2 3; do SIZE=1536x1024 python3 $G $P/pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6 7}; do echo "c$i: $(head -c 200 g$i.log)"; done
