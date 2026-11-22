# #14 SCOTUS: regenerate the heaven panel (6) as a three-way high five with Rabbi Joshua in his canon look.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=$(cd ~/g/git.debedb/pandeomonium/tools/pandeomonium && pwd)/gen212.py; P=$(cd "$(dirname "$0")" && pwd)
cd ~/g/git.debedb/pandeomonium-renders/scotus
for k in 1 2 3; do SIZE=1024x1536 python3 $G $P/p6.txt c6${1:-}.png p6ref.png joshua75.png > g6.log 2>&1 && break; sleep 20; done
head -c 300 g6.log
