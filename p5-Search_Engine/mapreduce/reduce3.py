#!/usr/bin/python3

import sys
import collections

wordDict = {}
infoDict = {}
count = 0
for line in sys.stdin:
	if line[len(line) - 1] == '\n':
		line = line[:-1]
	words = line.split()
	occurence = float(words[5])
	if words[0] not in wordDict:
		wordDict[words[0]] = occurence
	else:
		wordDict[words[0]] += occurence
	words.pop()
	infoDict[count] = words
	count = count + 1

sortedDict = collections.OrderedDict(sorted(wordDict.items()))
for key in infoDict:
	value = infoDict[key]
	word = value[0]
	del value[0]
	print (word, "\t", " ".join(infoDict[key]), " ", sortedDict[word])

    