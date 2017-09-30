#!/usr/bin/python3

import sys

for line in sys.stdin:
	words = line.split()
	idf = float(words[3])
	tf = float(words[2])
	factor = (idf * tf) * (idf * tf)
	word = words[0]
	del words[0]
	words.pop()
	print(word, "\t", " ".join(words), " ", factor)
