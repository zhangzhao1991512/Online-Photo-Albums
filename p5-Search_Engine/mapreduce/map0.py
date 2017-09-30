#!/usr/bin/python3

import sys

count = 0

for line in sys.stdin:	
	count = count + 1
	if count % 3 == 1:
		print("doc\t1")
