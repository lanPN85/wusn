#!/usr/bin/env bash

set -e

OUT_DIR=./out/kmxf/full
DATA_DIR=./data
RUNS=10

if [ ! -d "$OUT_DIR" ]; then
            mkdir -p ${OUT_DIR}
fi
echo > "$OUT_DIR/log.txt"

for it in $(seq 1 ${RUNS})
do
    echo "Run $it"
    for fn in "$DATA_DIR"/*.test
    do
        cmd="python3 kmxf.py -i $fn -o "${OUT_DIR}/run-${it}" --runs 1 --km-runs 1 2>>$OUT_DIR/log.txt"

        echo "$cmd"
        eval ${cmd}
        echo
    done
done
