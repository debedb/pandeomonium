set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
for i in 1 2 3 4 5 6 7 8; do SIZE=1024x1024 python3 ../pandeomonium/gen212.py pr-$i.txt c$i-a.png ../p220/s220-1a.png > g$i.log 2>&1 & done
wait
