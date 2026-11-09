set -a; . ~/.bash_profile >/dev/null 2>&1; set +a
R=../p220/s220-1a.png
SIZE=1024x1024 python3 ../pandeomonium/gen212.py pr-1b.txt c1-b.png $R > h1.log 2>&1 &
SIZE=1024x1024 python3 ../pandeomonium/gen212.py pr-4b.txt c4-b.png $R > h4.log 2>&1 &
SIZE=1024x1024 python3 ../pandeomonium/gen212.py pr-6b.txt c6-b.png c3-b.png $R > h6.log 2>&1 &
SIZE=1536x1024 python3 ../pandeomonium/gen212.py pr-7b.txt c7-b.png $R > h7.log 2>&1 &
wait
ls -la c1-b.png c4-b.png c6-b.png c7-b.png; tail -n 2 h*.log
