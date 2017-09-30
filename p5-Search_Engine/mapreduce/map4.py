#!/usr/bin/python3

import sys

for line in sys.stdin:
    info = line.split()
    print(info[1] + "\t" + info[0] + " " + info[2] + " " + info[3] + " " + info[4] + " " + info[5])
