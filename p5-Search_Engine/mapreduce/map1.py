#!/usr/bin/python3

import sys
import re



stopwords = []
f = open('./stopwords.txt', 'r')
for line in f.readlines():
	stopwords.append(line[:-1])

#-----------------------------------
count = 1
id = 0
for line in sys.stdin:
	line = re.sub(r'[^ a-zA-Z0-9]+', '', line).lower()
	if count % 3 == 1:
		id = line.split()[0]
	else:
		words = [word for word in line.split() if word not in stopwords]
		for word in words:
			print(word, "\t", id, " ", "1")
	count = count + 1
        

