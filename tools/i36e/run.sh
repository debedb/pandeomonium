# #36 engineering deck: seven panels (the last one wide) in parallel, each with its likeness references; retries on transient errors. Args select panels.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd); R=$HOME/g/git.debedb/pandeomonium-renders/enterprise/refs
mkdir -p ~/g/git.debedb/pandeomonium-renders/enterprise/eng; cd ~/g/git.debedb/pandeomonium-renders/enterprise/eng
refs(){ case $1 in
  [1-6]) echo $R/euler.png $R/geordi.png;;
  7) echo $R/geordi.png $R/euler.png;;
esac; }
for i in ${@:-1 2 3 4 5 6 7}; do
  cat $P/style.txt $P/p$i.txt > pr-$i.txt
  (for k in 1 2 3; do SIZE=1536x1024 python3 $G pr-$i.txt c$i.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
for i in ${@:-1 2 3 4 5 6 7}; do echo "c$i: $(head -c 200 g$i.log)"; done
