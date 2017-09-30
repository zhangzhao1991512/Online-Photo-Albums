#!/usr/bin/python3

import sys

count = 0
for line in sys.stdin:
	count = count + 1

f = open('./total_document_count.txt', 'wt')
f.write(str(count))
f.close()

print (count)

