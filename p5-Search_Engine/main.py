from flask import *
import config
#import requests
import re
import math
#import json

import operator
main = Blueprint('main', __name__, template_folder='templates')

stopwords = []
with open('stopwords.txt', 'r') as data1:
    for line in data1:
        stopwords.append(line.rstrip())

tdidf = []
with open("outfile.txt", "r") as data2:
#with open("sample.txt", "r") as data2:
    #index_pool = data2.readline()
    #for line in index_pool:
    for line in data2:
        line = line.strip('\n')
        l = len(line.split())
        #print line
        #print l
        key = line.split()[0]
        idf = line.split()[1]
        val = []
        i = 3
        while i < l:
            tmp = {"id": line.split()[i], "tf": line.split()[i+1], "norm": line.split()[i+2]}
            val.append(tmp)
            i = i + 3
        tdidf.append({"key": key, "idf":idf, "val": val})

pagerank = []
with open("pagerank.out", "r") as data3:
#with open("p.out", "r") as data3:
    #pagerank_pool = data3.readline()
    #for line in pagerank_pool:
    for line in data3:
        line = line.strip('\n')
        #print line
        docid = line.split(',')[0]
        rank = line.split(',')[1]
        tmp = {"docid": docid, "rank": rank}
        pagerank.append(tmp)

@main.route('/', methods = ['GET'])
def main_route():
    query = request.args.get('q')
    weight = request.args.get('w')
    print query + " " + weight

#    response = json.jsonify({"hits":[{"docid": 1, "score": 0.5}] })
#    return response
    words = []
    query = query.strip()
    q = query.split(' ')
    #GET ALL WORDS
    for word in q:
        #print word
        #if not word.isalnum():  # Remove non-alphanumeric characters
        word = re.sub(r'[^a-zA-Z0-9]+', '', word)
        word = word.lower()  # Convert to lowercase 
        if word not in stopwords and len(word) > 0:
            add = True
            for tmp in words:
                if tmp['word'] == word:
                    tmp['tf'] += 1
                    add = False
                    break
            if add:
                words.append({"word": word, "tf": 1})
        print word
    
    print words
    print "finish get all words"

    useful = []
    #Find all relavant docs
    for tmp in tdidf:
        if len(useful) == len(words):
            break
        for tmp2 in words:
            if tmp['key'] == tmp2['word']:
                useful.append(tmp)
                break

####################################################
    if len(useful) < len(words):
        response = json.jsonify({"hits":[]})
        return response
####################################################

    print useful

    rel_docid = []
    cnt = 0
    while cnt < len(useful):
        if cnt == 0:
            tmp = useful[cnt]['val']
            for t in tmp:
                rel_docid.append(t['id'])
        else:
            tmp = useful[cnt]['val']
            for t in rel_docid:
                thisone = t
                buzai = True
                for t1 in tmp:
                    if t == t1['id']:
                        buzai = False
                        break
                if buzai:
                    rel_docid.remove(thisone)
        cnt = cnt + 1

    print rel_docid
    print "start calculation"
    docs = []
    #COMPUTE ALL INDEX...
    for thisid in rel_docid:
        #pagerank
        thisrank = 0.0
        for r in pagerank:
            if thisid == r['docid']: 
                thisrank = float (r['rank'])
        if thisrank > 0:
            print "has pagerank"
        else:
            print "sth wrong... cannot find pagerank"

        doclength = 0.0
        querylength = 0.0
        count = 0.0
        #iterate all the words  ##########start calculation
        for word in words:
            for tmp in useful:
                if tmp['key'] == word['word']:
                    idf = float(tmp['idf'])
                    querylength = querylength + idf * idf * float(word['tf']) * float (word['tf'])
                    tmpval = tmp['val']
                    for i in tmpval:
                        if i['id'] == thisid:
                            count = count + idf * idf * float(i['tf']) * float(word['tf'])
                            doclength = float (i['norm'])
        ##################finish calculation############################
        if querylength > 0 and doclength > 0 and count > 0:
            l1 = math.sqrt(querylength)
            l2 = math.sqrt(doclength)
            #l1 = querylength**(1.0/2)
            #l2 = doclength**(1.0/2)
            w = float (weight)
            score = w * thisrank + (1.0-w) * count / (l1*l2)
            docs.append({"docid": thisid, "score": score})
        else:
            print "Calculation WRONG!"

    print docs
    ##############SORT ALL THE RELAVENT DOCUMENTS################3
    newdocs = sorted(docs, key=lambda k: k['score']) 

    print newdocs

    temp = {}
    temp["hits"] = newdocs
    #print "json......"
    response = json.jsonify(temp)
    print response
    print "Ok, lets return response"
    return response
