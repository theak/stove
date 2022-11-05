#!/bin/bash
for i in {1..11}; do python3 ~/opencv/main.py &>> ~/opencv/log.txt && sleep 4; done


