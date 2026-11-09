set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
P=../pandeomonium
python3 $P/gen212.py pr-p9b.txt p9-b.png ref-swiss.png ref-pleischner.png > j1.log 2>&1 &
python3 $P/gen212.py pr-met2.txt met-a.png ref-met.png ref-swiss.png ref-mm.png > j2.log 2>&1
python3 $P/gen212.py pr-pan.txt pan-a.png met-a.png > j3.log 2>&1
wait
