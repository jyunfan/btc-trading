#!/bin/bash
echo $@
while true
do
../env/bin/python rebalance.py $@
sleep 600
done
