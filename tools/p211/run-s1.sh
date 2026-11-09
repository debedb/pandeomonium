source ~/.bash_profile >/dev/null 2>&1; test -n "$OPENAI_API_KEY" || exit 9
M=../pandeomonium/maskfix211.py
r() { "$@" || "$@"; }
set -e
export SOFTEN=0.6
r python3 $M s211-1m3.png 900 661 1250 1011 1008 664 1142 792 ref-daneel.png s211-1d.png "Edit the FIRST image only. Repaint ONLY the transparent area of the mask: the head of the young man in the black suit standing beside the police captain, looking down at the table. Make his face and hair exactly the same man as in the SECOND image (R. Daneel Olivaw: young, short neat brown hair swept back, smooth grave handsome face). Keep the exact head position, size, tilt and downward gaze, and match the warm amber lighting, soft focus, grain and colour grading. No text."
export SOFTEN=0.4
CAPA='Edit the FIRST image only. Repaint ONLY the transparent area of the mask: change the white dinner jacket of the man with slicked dark hair and a black bow tie into a BLACK dinner jacket with satin lapels, same cut, folds and fit. Keep his face, hands, cigar, white shirt and black bow tie exactly, and everything else unchanged. Match lighting, grain and colour grading. No text.'
r python3 $M s211-1d.png 400 0 780 345 455 140 715 245 - s211-1e.png "$CAPA"
r python3 $M s211-1e.png 1030 0 1536 345 1045 150 1410 248 - s211-1e.png "$CAPA"
r python3 $M s211-1e.png 435 355 795 655 435 505 705 580 - s211-1e.png "$CAPA"
r python3 $M s211-1e.png 300 760 900 1024 360 880 820 1024 - s211-1e.png "Edit the FIRST image only. Repaint ONLY the transparent area of the mask: the man seen from behind in a white dinner jacket must wear a BLACK dinner jacket instead, same shoulders, cut and pose, seen from behind. Keep his hair and everything else unchanged. Match lighting, grain and colour grading. No text."
echo strip1-done
