#!/usr/bin/env bash
rm small_data/*.test
python3 datagen2.py -o small_data/ -W 200 -H 200 -M 20 -N 20 -Y 4
