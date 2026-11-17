# #27 IKEA strip: masked repaints of panels 2, 4 and 8 on the first render; everything outside the masks stays as rendered.
# Panels 2, 4 and the panel-8 face run in parallel on src.png; the panel-8 handcuffs run on the face result; assemble.py merges.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
M=$(cd ../pandeomonium && pwd)/maskfix211.py; P=$(pwd); R=~/g/git.debedb/pandeomonium-renders/ikea
fix(){ for k in 1 2 3; do python3 $M "$@" > "g-$(basename ${@: -2:1} .png).log" 2>&1 && return; sleep 20; done; return 1; }
cd $R
fix src.png 255 272 511 528  300 272 505 378  refs/goering_face.png      o2.png  "$(cat $P/pr-2.txt)" &
fix src.png 0 567 360 927    130 567 275 700  refs/tikhonov_p3.png  o4.png  "$(cat $P/pr-4.txt)" &
(fix src.png 760 1190 1019 1449  815 1240 905 1345  refs/myagkov_gonki.png  o8a.png "$(cat $P/pr-8a.txt)" &&
 fix o8a.png 600 1112 1019 1531  620 1340 1019 1531  -  o8.png "$(cat $P/pr-8b.txt)") &
wait
ls -la o2.png o4.png o8a.png o8.png; for f in g-*.log; do echo "$f: $(head -c 200 $f)"; done
