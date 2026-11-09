# Strip 2 of #1 (bathroom window): 3 square + 4 wide panels, in parallel.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=../pandeomonium/gen212.py
for i in 1 2 3; do SIZE=1024x1024 python3 $G pr-$i.txt c$i-a.png ref-ronin.png ref-sketchC.png > g$i.log 2>&1 & done
for i in 4 5 6; do SIZE=1536x1024 python3 $G pr-$i.txt c$i-a.png ref-ronin.png ref-sketchC.png > g$i.log 2>&1 & done
SIZE=1536x1024 python3 $G pr-7.txt c7-a.png ref-ronin.png ref-sketchC.png ref-cafe.png > g7.log 2>&1 &
wait
ls -la c?-a.png; tail -n 1 g*.log
