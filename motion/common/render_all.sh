#!/usr/bin/env bash
# render all three TCMG videos in parallel, then mux with their mixes and make the 4:5 crops
set -euo pipefail
M=/home/user/1stTask/motion
for d in tcmg-schools-v2 tcmg-cost-v2 tcmg-commute-v2; do node $M/$d/render.js video > $M/$d/render.log 2>&1 & done; wait
mux(){ d=$1; name=$2; cd $M/$d
  ffmpeg -v error -y -i video_only.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest REVIEW/$name-9x16.mp4
  ffmpeg -v error -y -i REVIEW/$name-9x16.mp4 -vf "crop=1080:1350:0:285" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy REVIEW/$name-4x5.mp4; }
mux tcmg-schools-v2 07-tcmg-schools-catchment-v6
mux tcmg-cost-v2 05-tcmg-cost-what-does-a-home-cost-v4
mux tcmg-commute-v2 05-tcmg-commute-test-the-commute-v4
echo ALL DONE
