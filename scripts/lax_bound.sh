#!/usr/bin/env bash

set -e

TARGET_DIR=./medium_data
OUT_DIR=./out/lb/medium

echo > ${TARGET_DIR}/BOUND
for fn in "$TARGET_DIR"/*.test
    do
        cmd="python3 lp_solve.py --lax -i $fn -o "${OUT_DIR}" 2>>$TARGET_DIR/BOUND"

        echo "$cmd"
        eval ${cmd}
        echo
done
