#!/bin/bash
while true
do
    echo "Start trading"
    python trading.py ~/.bitstamp/key
    sleep 300
done
