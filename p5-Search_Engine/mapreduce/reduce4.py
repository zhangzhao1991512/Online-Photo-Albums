#!/usr/bin/python3

import sys

infoDict = {}
count = 0

for line in sys.stdin:
	if line[len(line) - 1] == '\n':
		line = line[:-1]
	words = line.split()
	if words[0] in infoDict:
		infoDict[words[0]].append(words[1])
		infoDict[words[0]].append(words[2])
		infoDict[words[0]].append(words[5])
	else:
		info = []
		info.append(words[3])
		info.append(words[4])
		info.append(words[1])
		info.append(words[2])
		info.append(words[5])
		infoDict[words[0]] = info
	count = count + 1

for key in infoDict:
    #print ("\t".join(infoDict[key]), "\t", sortedDict[infoDict[key][0]])    
    #f = open("./mapreduce/output/invert_index.txt",'a')
    #f.write(key)
    #f.write("\t")
    #f.write(" ".join(infoDict[key]))
    #f.write('\n')
    #f.close()
    print (key, "\t", " ".join(infoDict[key]))
