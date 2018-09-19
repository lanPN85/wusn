#!/usr/bin/env bash

set -e

OUT_DIR=./out/mxf_k/full
DATA_DIR=./data/cer
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
        cmd="python3 k_mxf_ga.py -i $fn -o "${OUT_DIR}/run-${it}" 2>>$OUT_DIR/log-cer.txt"

        echo "$cmd"
        eval ${cmd}
        echo
    done
done
