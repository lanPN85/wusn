#!/usr/bin/env bash

set -e

DATA_DIR=./data
DATA_SIZE=full
ROOT_DIR=./out/kmh
RUNS=20

for lb in 0 1 2 3; do
    OUT_DIR=${ROOT_DIR}/lb${lb}/${DATA_SIZE}
    if [ ! -d "$OUT_DIR" ]; then
        mkdir ${OUT_DIR}
    fi
    echo > "$OUT_DIR/log.txt"

    for it in $(seq 1 ${RUNS})
    do
        echo "Run $it"
        for fn in "$DATA_DIR"/*.test
        do
            cmd="python3 km_heuristic.py -i $fn -o "${OUT_DIR}/run-${it}" --lb ${lb} 2>>$OUT_DIR/log.txt"

            echo "$cmd"
            eval ${cmd}
            echo
        done
    done
done
