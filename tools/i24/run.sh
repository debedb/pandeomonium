# #24 real estate office: five panels in parallel with film stills / established likenesses as references; retries on transient errors.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=../pandeomonium/gen212.py; R=~/g/git.debedb/pandeomonium-renders/i24-refs
refs(){ case $1 in
  1) echo $R/blake_face.png $R/blake_suit.png $R/moss.png;;
  2) echo $R/blake_suit.png $R/moss.png $R/levene.png $R/eco.png;;
  3) echo $R/blake_face.png $R/blake_suit.png $R/koons.png;;
  4) echo $R/koons.png $R/eco.png $R/blake_suit.png;;
  5) echo $R/kant1.png $R/kant2.png;;
esac; }
for i in 1 2 3 4 5; do
  (for k in 1 2 3; do SIZE=1536x1024 python3 $G pr-$i.txt c$i-a.png $(refs $i) > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
ls -la c?-a.png; for f in g*.log; do echo "$f: $(head -c 200 $f)"; done
