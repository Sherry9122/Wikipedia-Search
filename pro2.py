import math

def pageRank(dic, revdic):
    i = 0
    PR = {}
    pages = getpages(dic)

    # N is the number of whole pages
    N = len(dic)

    # initial value
    for p in pages:
        PR[p] = 1/float(N)

    newPR = {}
    counter = 0
    newperplexity = 0
    perplexity = calper(PR, 1)
    s = calculateS(dic, revdic)
    while abs(newperplexity - perplexity) > 1 or counter <= 4:
        if abs(newperplexity - perplexity) < 1:
            counter = counter + 1
            print "counter: " + str(counter)
        # calculate total sink PR
        perplexity = newperplexity
        sinkPR = 0
        for p in s:
            sinkPR = sinkPR + PR[p]
        print "after sinknode"
        for p in pages:
            # print "calculate" + str(p)
            #  teleportation
            newPR[p] = (1 - 0.85) / float(N)
            # spread remaining sink PR evenly
            newPR[p] = newPR[p] + 0.85 * sinkPR / float(N)
            # pages pointing to p, no duplicate
            pointto = dic[p]
            for q in pointto:
                # add share of PageRank from in-links
                lq = caloutlink(revdic, q)
                newPR[p] = newPR[p] + 0.85 * PR[q] / lq
        for p in pages:
             PR[p] = newPR[p]
        newperplexity = calper(PR, 1)
        # print PR
    return PR

def dealgraph():
    dic = {}
    fo = open("G2.txt", "r")
    urls = fo.readlines()
    for line in urls:
        line = line.split('\n')[0]
        # print "read line"
        line = line.split(' ')
        dic[str(line[0])] = []
        i = 1
        while i < len(line):
            if len(str(line[i])) > 0:
                dic[str(line[0])].append(str(line[i]))
                i = i + 1
            else:
                i = i + 1
                continue
    for key in dic:
        dic[key] = list(set(dic[key]))
    print "done with graph"
    return dic

def reversedic(dic):
    # print "in reverse fuction"
    revdic = {}
    for key in dic:
        # print "key is:" + key
        for value in dic[key]:
            # print "value is : " + value
            # print revdic.has_key(value)
            if revdic.has_key(value):
                # print "writing revdic"
                revdic[value].append(key)
            else:
                # print "creating new key value pair"
                revdic[value] = [key]
    print "done reverse"
    return revdic


# get the first column of the test file
def getpages(dic):
    list = []
    for key in dic:
        list.append(key)
    # print "get key" + str(list)
    return list

# calpture the perplexity of all the pagerank
def calper(PR, counter):
    add = 0
    perplexity = 0
    if counter is 0:
        return 1000
    else:
        for pagerank in PR:
            add = add + PR.get(pagerank) * math.log(PR.get(pagerank), 2)
        perplexity = math.pow(2, -add)
    fo = open("PRG2.txt", "a")
    writing = "perplexity is : " + str(perplexity)
    fo.write(writing + '\n')
    print writing
    return perplexity


# get the set of all the sink nodes
def calculateS(dic, revdic):
    keys = dic.keys()
    revkey = revdic.keys()
    listall = keys
    for ele in revkey:
        listall.remove(ele)
    print "sinknode"
    return listall


def caloutlink(revdic, q):
    return len(revdic[q])

def writeresult(result):
    fo = open("PRG2.txt", "a")
    fo.write('\n')
    print "printing result"
    sortedresult = sorted(result.items(), key=lambda x: x[1], reverse = True)
    print sortedresult[0]
    i = 0
    for key in sortedresult:
        # print "key is " + str(key)
        string = str(sortedresult[i]).split(')')[0]
        string = string.split('(')[1]
        fo.write(string + '\n')
        # print "value is " + str(result[key])
        i = i + 1
    fo.close()


dic = dealgraph()
revdic = reversedic(dic)
result = pageRank(dic, revdic)
print result
writeresult(result)