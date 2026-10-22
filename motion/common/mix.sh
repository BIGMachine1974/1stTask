#!/usr/bin/env bash
# usage: mix.sh <project dir> <duration seconds>  -> <dir>/mix.wav at -15 LUFS (VO on top, SFX under, bed about 19 dB under VO)
set -euo pipefail
D=$1; DUR=$2; cd "$D"
FO=$(python3 -c "print($DUR-1.5)")
ffmpeg -v error -y -i bed_c.mp3 -i bed_c.mp3 -filter_complex \
 "[0]aresample=48000,volume='if(lt(t,9.6),1.6,if(lt(t,10.6),1.6-0.6*(t-9.6),1))':eval=frame[a];[1]aresample=48000,atrim=start=12,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=2.5:c1=tri:c2=tri,afade=t=in:d=0.6,afade=t=out:st=$FO:d=1.5,atrim=0:$DUR[m]" \
 -map "[m]" bed_shaped.wav
ffmpeg -v error -y -i vo.mp3 -i sfx.wav -i bed_shaped.wav -filter_complex \
 "[0]aresample=48000,apad=whole_dur=$DUR[v];[1]volume=0.3[s];[2]volume=-23dB[b];[v][s][b]amix=inputs=3:duration=longest:normalize=0[m]" \
 -map "[m]" -t "$DUR" -c:a pcm_s16le mix_raw.wav
J=$(ffmpeg -hide_banner -i mix_raw.wav -af loudnorm=I=-15:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
MI=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i mix_raw.wav -af "loudnorm=I=-15:TP=-1:LRA=11:$MI:linear=true,aresample=48000" mix.wav
rm -f mix_raw.wav
ffmpeg -hide_banner -i mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I:|Peak:)' | tail -2
