#!/usr/bin/env bash

set -e

DATA_DIR=./medium_data
OUT_DIR=./out/yuan/best/medium

if [ ! -d "$OUT_DIR" ]; then
     mkdir -p ${OUT_DIR}
fi


echo > "$OUT_DIR/log.txt"

for fn in "$DATA_DIR"/*.test
do
    cmd="python3 yuan_best.py -i $fn -o $OUT_DIR 2>>$OUT_DIR/log.txt"
    echo "$cmd"
    eval ${cmd}
    echo
done
