# Strip 1 of #1 (Draw It Again): generate six square panels in parallel.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=../pandeomonium/gen212.py
for i in 1 2 3 4 5 6; do
  refs=ref-ronin.png; [ $i = 1 ] && refs="ref-ronin.png ref-sketchA.png"
  SIZE=1024x1024 python3 $G pr-$i.txt c$i-a.png $refs > g$i.log 2>&1 &
done
wait
ls -la c?-a.png; tail -n 1 g*.log
