#!/usr/bin/python3

import sys
import collections

wordcountDict = {}
infoDict = {}
count = 0
newdoc = 0
totalnum = 0
for line in sys.stdin:
	if line[len(line) - 1] == '\n':
		line = line[:-1]
	word = line.split("\t")[0]
	value = line.split("\t")[1]
	words = value.split(" ")
	words.insert(0, word)
	infoDict[count] = words
	if words[0] in wordcountDict:
		wordcountDict[words[0]] += int(words[2])
		totalnum = wordcountDict[words[0]]
	else:
		for num in range(newdoc, count):
			infoDict[num].append(str(int(infoDict[num][2])))				
		newdoc = count
		wordcountDict[words[0]] = 1
	count = count + 1

for num in range(newdoc, count):
			infoDict[num].append(str(int(infoDict[num][2])/totalnum))

sortedDict = collections.OrderedDict(sorted(wordcountDict.items()))
for key in infoDict:
    #print ("\t".join(infoDict[key]), "\t", sortedDict[infoDict[key][0]])
	print ("\t".join(infoDict[key]))