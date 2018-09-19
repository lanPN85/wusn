#!/usr/bin/env bash

set -e

OUT_DIR=./out/prop3_1-random/medium
DATA_DIR=./medium_data
RUNS=20

if [ ! -d "$OUT_DIR" ]; then
            mkdir ${OUT_DIR}
fi
echo > "$OUT_DIR/log.txt"

for it in $(seq 1 ${RUNS})
do
    echo "Run $it"
    for fn in "$DATA_DIR"/*.test
    do
        cmd="python3 prop3_1.py -i $fn -o "${OUT_DIR}/run-${it}" --pop-size 200 --patience 30 --init random 2>>$OUT_DIR/log.txt"

        echo "$cmd"
        eval ${cmd}
        echo
    done
done
