#!/usr/bin/python3

import sys
import collections
import math

wordDict = {}
wordDocList = []
for line in sys.stdin:
    word = line.split()[0]
    doc = line.split()[1]
    if word in wordDict:
        #wordDict[word] += 1
        theWordDoc = next(item for item in wordDocList if item['word'] == word)
        theWordDoc['totalNum'] += 1
        theDocList = theWordDoc['doc']
        for document in theDocList:
            if document['doc'] == doc:
                document['ocurNum'] += 1
                docExist = True
                break
            else:
                docExist = False
        if not docExist:
            docDic = {"doc" : doc,
                            "ocurNum" : 1}
            theDocList.append(docDic)
            
            
        
    else: #a new wordDict
        wordDict[word] = 1
        docList = []
        docDic = {"doc": doc,
                        "ocurNum" : 1}
        docList.append(docDic)
        wordDocDict = {"word" : word,
                                 "doc" : docList,
                                 "totalNum" : 1}
        wordDocList.append(wordDocDict)
        

sortedDict = collections.OrderedDict(sorted(wordDict.items()))
#print(sortedDict)
'''for key in sortedDict:
    print (key, sortedDict[key])
'''
#print(wordDocList)

f = open('./total_document_count.txt', 'rt')
data = f.read()
N = int(data)
f.close()

for theWord in wordDocList:
    nk = len(theWord['doc'])
    idf = math.log10(float(N)/float(nk))
    for theDoc in theWord['doc']:
        print(theWord['word'],"\t",theDoc['doc']," ",theDoc['ocurNum']," ",idf," ",theWord['totalNum'])
