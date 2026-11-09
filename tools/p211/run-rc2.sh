
source ~/.bash_profile >/dev/null 2>&1; test -n "$OPENAI_API_KEY"
M=../pandeomonium/maskfix211.py
export SOFTEN=0.5
RICK='Repaint ONLY the transparent area of the mask: the head of the man in the white dinner jacket and black bow tie, who is Rick Blaine. Make his face exactly the same man as in the SECOND image (a Humphrey Bogart likeness: lean weathered face, heavy-lidded eyes, slicked-back receding dark hair). Keep the exact head position, size, angle, gaze, expression direction and focus/blur level of the original; if he is out of focus in the background, keep him equally out of focus. Match lighting, grain and colour grading. Edit the FIRST image only; no text, no speech balloons.'
r() { "$@" || "$@"; }
set -e
# strip 3: panels 1 and 3
r python3 $M s211-y2.png 60 0 400 340 140 15 255 145 ref-rick.png s211-z2.png "$RICK"
r python3 $M s211-z2.png 60 512 400 852 145 520 265 650 ref-rick.png s211-z2.png "$RICK"
# strip 1: Capablanca's jacket white -> black
CAPA='Repaint ONLY the transparent area of the mask: change the white dinner jacket of the man with slicked dark hair and a black bow tie into a BLACK dinner jacket with satin lapels, same cut, folds and fit. Keep his face, hands, cigar, white shirt and black bow tie exactly as they are, and keep everything else unchanged. Match the lighting, grain and colour grading. No text.'
r python3 $M s211-1m3.png 400 0 780 345 455 140 715 245 - s211-1c.png "$CAPA"
r python3 $M s211-1c.png 1030 0 1536 345 1045 150 1410 248 - s211-1c.png "$CAPA"
r python3 $M s211-1c.png 435 355 795 655 435 505 705 580 - s211-1c.png "$CAPA"
r python3 $M s211-1c.png 300 760 900 1024 360 880 820 1024 - s211-1c.png "Repaint ONLY the transparent area of the mask: the man seen from behind in a white dinner jacket must wear a BLACK dinner jacket instead, same shoulders, cut and pose, seen from behind. Keep his hair and everything else unchanged. Match the lighting, grain and colour grading. No text."
echo done
