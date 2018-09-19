#!/usr/bin/env bash
rm medium_data/*.test
python3 datagen2.py -o medium_data/ -W 500 -H 500 -M 100 -N 100 -Y 10
