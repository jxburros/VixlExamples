#!/bin/bash
# usage: sheet.sh video out.png t1 t2 ... (seconds) -> contact sheet 3 columns
v=$1; out=$2; shift 2
tmp=$(mktemp -d); i=0
for t in "$@"; do ffmpeg -loglevel error -y -ss $t -i "$v" -frames:v 1 -vf scale=640:-1 $tmp/f$(printf %03d $i).png; i=$((i+1)); done
cols=3; rows=$(( (i+cols-1)/cols ))
ffmpeg -loglevel error -y -pattern_type glob -i "$tmp/f*.png" -vf "tile=${cols}x${rows}" -frames:v 1 "$out"
rm -rf $tmp
