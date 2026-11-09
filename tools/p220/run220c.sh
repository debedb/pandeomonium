set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
P=../pandeomonium
FEATHER=4 python3 $P/maskfix211.py s220-1a.png 190 100 690 600 298 209 582 375 ref-chgk2.png tile5-d.png "$(cat pr-tile5d.txt)" > m1.log 2>&1 &
python3 $P/gen212.py pr-p345e.txt p345-e.png p4-b.png ref-gorb.png > m2.log 2>&1
wait
