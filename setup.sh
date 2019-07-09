#!/usr/bin/env sh

if [ ! -d "sat" ]; then
    python3 -m venv env
fi
sleep 1
source ./env/bin/activate
pip3 install -r requirements.txt
reprobench --version

