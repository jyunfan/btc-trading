#!/bin/bash
while true
do
    echo "Start recording"
    python recorder.py $@
    sleep 10
done
