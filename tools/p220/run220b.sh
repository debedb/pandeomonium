set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
P=../pandeomonium
python3 $P/maskfix211.py gate-a.png 190 100 690 600 296 207 584 377 ref-chgk1.png tile5-b.png "$(cat pr-tile5.txt)" > k1.log 2>&1 &
python3 $P/gen212.py pr-p4.txt p4-b.png ref-gate.png ref-gorb.png > k3.log 2>&1 &
python3 $P/gen212.py pr-p3.txt p3-b.png ref-gate.png ref-gate87.png gate-a.png > k2.log 2>&1
python3 $P/gen212.py pr-p567.txt p567-b.png p3-b.png ref-gorb.png > k4.log 2>&1
wait
