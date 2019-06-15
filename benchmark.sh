#!/usr/bin/env sh

reprobench server &
rm -rf output
reprobench bootstrap && reprobench manage local run
killall reprobench

