#!/usr/bin/env bash

set -e

DATA_DIR=./data
DATA_SIZE=full
ROOT_DIR=./out/hxf

for lu in 1 2; do
    OUT_DIR=${ROOT_DIR}/lu${lu}/${DATA_SIZE}
    if [ ! -d "$OUT_DIR" ]; then
        mkdir ${OUT_DIR}
    fi
    echo > "$OUT_DIR/log.txt"

    for fn in "$DATA_DIR"/*.test
    do
        cmd="python3 hxf.py -i $fn -o "${OUT_DIR}" --lu ${lu} 2>>$OUT_DIR/log.txt"

        echo "$cmd"
        eval ${cmd}
        echo
    done
done
