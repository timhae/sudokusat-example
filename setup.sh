#!/usr/bin/env sh

if [ ! -d "sat" ]; then
    python3 -m venv sat
fi
sleep 1
source ./sat/bin/activate
pip3 install -r requirements.txt
reprobench --version

