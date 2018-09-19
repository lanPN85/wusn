#!/usr/bin/env bash

set -e

<<<<<<< HEAD

DATA_DIR=./medium_data
OUT_DIR=./out/yuan/best/medium
=======
DATA_DIR=./small_data
OUT_DIR=./out/yuan/best/small
>>>>>>> de84843293ed742e204aa176d2e2acc81bfbec65

if [ ! -d "$OUT_DIR" ]; then
            mkdir ${OUT_DIR}
fi


echo > "$OUT_DIR/log.txt"

for fn in "$DATA_DIR"/*.test
do
    cmd="python3 yuan_best.py -i $fn -o $OUT_DIR 2>>$OUT_DIR/log.txt"
    echo "$cmd"
    eval ${cmd}
    echo
done
