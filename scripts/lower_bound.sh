#!/usr/bin/env bash

set -e

TARGET_DIR=./medium_data
OUT_DIR=./out/exact/medium

echo > ${TARGET_DIR}/OPTIMAL
for fn in "$TARGET_DIR"/*.test
    do
        cmd="python3 lp_solve.py -i $fn -o "${OUT_DIR}" 2>>$TARGET_DIR/OPTIMAL"

        echo "$cmd"
        eval ${cmd}
        echo
done
