source ~/.bash_profile >/dev/null 2>&1; test -n "$OPENAI_API_KEY" || exit 9
M=../pandeomonium/maskfix211.py
r() { "$@" || "$@"; }
set -e
export SOFTEN=0.5
RICK='Edit the FIRST image only. Repaint ONLY the transparent area of the mask: the head of the man in the white dinner jacket and black bow tie, Rick Blaine. Make his face exactly the same man as in the SECOND image (Humphrey Bogart likeness: lean weathered face, heavy-lidded eyes, slicked-back receding dark hair, cigarette). Keep the exact head position, size, angle and gaze. Match lighting, grain and colour grading. No text.'
r python3 $M s211-y2.png 60 0 400 340 140 15 255 145 ref-rick.png s211-s3.png "$RICK"
r python3 $M s211-s3.png 60 512 400 852 145 520 265 650 ref-rick.png s211-s3.png "$RICK"
LANDA='Edit the FIRST image only. Repaint ONLY the transparent area of the mask: the head of the German colonel on the telephone. He is Colonel Hans Landa as played by Christoph Waltz in Inglourious Basterds, and must be a strong likeness of Christoph Waltz in that role: Austrian, about fifty, lean narrow face, high forehead, dark hair slicked straight back, pale blue-grey eyes, thin arched eyebrows, and the famous Landa expression: a huge, delighted, theatrical, overly polite grin full of menace and charm, eyebrows raised high, savouring the moment. Keep the receiver at his ear, the head position and size. Match lighting, grain and colour grading. No text.'
r python3 $M s211-s3.png 1030 0 1536 505 1150 0 1360 230 - s211-s3.png "$LANDA"
r python3 $M s211-s3.png 1030 512 1536 1024 1150 520 1360 740 - s211-s3.png "$LANDA"
echo strip3-faces-done
