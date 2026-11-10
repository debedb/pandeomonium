# Strip 4 of #1 (Sonnet 18 / author / Solomon): six panels in parallel, each with its sketch crop as reference; retries on transient errors.
set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
G=../pandeomonium/gen212.py
for i in 1 2 3 4 5 6; do
  size=1024x1024; case $i in 5|6) size=1536x1024;; esac
  refs="ref-sk$i.png"; [ $i = 3 ] && refs="ref-sk3.png c1-a.png"
  (for k in 1 2 3; do SIZE=$size python3 $G pr-$i.txt c$i-a.png $refs > g$i.log 2>&1 && break; sleep 20; done) &
done
wait
ls -la c?-a.png; for f in g*.log; do echo "$f: $(head -c 100 $f)"; done
