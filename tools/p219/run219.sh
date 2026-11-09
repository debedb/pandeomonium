set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
P=../pandeomonium
python3 $P/maskfix211.py ref-swiss.png 688 176 1536 1024 690 672 1534 1022 ref-pleischner.png p9-a.png "$(cat pr-p9.txt)" > j1.log 2>&1 &
python3 $P/gen212.py pr-met.txt met-a.png ref-met.png ref-swiss.png ref-mm.png > j2.log 2>&1 &
python3 $P/gen212.py pr-meet.txt meet-a.png ref-owl.png ref-knor-cat.png ref-knor.png ref-swiss.png > j4.log 2>&1 &
wait
python3 $P/gen212.py pr-pan.txt pan-a.png met-a.png > j3.log 2>&1
