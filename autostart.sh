#!/bin/sh
discord &
sleep 60
xterm -e python3 ~/Discord-ROIP/ptt.py &
