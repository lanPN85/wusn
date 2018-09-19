#!/usr/bin/env bash

set -e

OUT_DIR=./out/mxf_k/small-50
DATA_DIR=./small_data
RUNS=20

if [ ! -d "$OUT_DIR" ]; then
            mkdir ${OUT_DIR}
fi
echo > "$OUT_DIR/log.txt"

for it in $(seq 1 ${RUNS})
do
    echo "Run $it"
    for fn in "$DATA_DIR"/cer-*.test
    do
        cmd="python3 k_mxf_ga.py --pop-size 50 -i $fn -o "${OUT_DIR}/run-${it}" 2>>$OUT_DIR/log-cer.txt"

        echo "$cmd"
        eval ${cmd}
        echo
    done
done
