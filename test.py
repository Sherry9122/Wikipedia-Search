import time
import re
import string
import requests
from bs4 import BeautifulSoup

# task 1.1
# The function take in 3 variables, url is the hyperlink of the website that need to be crawled
# i is the number of the docid, it will link to the Wikipedia article
# the function will maintain and return a dictionary that contains all the docid corresponding with the article name
def content(url, i, filedic):
    try:
        url = url.split('\n')[0]
        r = requests.get(url)
        time.sleep(1)
        soup = BeautifulSoup(r.content)
        docid = "doc" + str(i)
        textname = filename(url)
        filedic[docid] = textname
        file = open(textname + ".txt", "w+")
        for paragraph in soup.find_all("p"):
            try:
                content = paragraph.text
                content = str(content).lower()
                words = content.split(" ")
                for word in words:
                    if patternmatch(word):
                        # punctuation that need to be retained(Task1.3)
                        continue
                    else:
                        if '[' in word and ']' in word:
                            word = word[0: word.index('[')]
                        # normal punctuation(Task1.3)
                        word = "".join(l for l in word if l not in string.punctuation)
                    file.write(str(word) + " ")
            except:
                continue
        file.close()
        return filedic
    except:
        return filedic

# task 1.2
# the input is a url and the function will return a file name that extract for the url as task1.2 asked
def filename(url):
    docid = url.split('/')
    # get the last word
    docid = docid[len(docid) - 1]
    # get rid of the enter'\n'
    docid = docid.split('\n')[0]
    if "_" in docid:
        docid = docid.replace("_", "")
    if "-" in docid:
        docid = docid.replace("-", "")
    return docid

# task 1.3
# the function will retain punctuation within digits
def patternmatch(string):
    pattern = re.compile(r'\d[, .]\d')
    pattern2 = re.compile('.\d')
    if pattern.match(string) or pattern2.match(string):
        # print "match"
        return True
    else:
        # print "not match"
        return False

# task2
# the input is the dictionary that task1 returned containing the docids and their corresponding text names
# the function will return a list that contains the inverted list when n = 1, 2, 3
def invertedindex(filedic):
    # dic1 stores the inverted index when n = 1
    # dic2 stores the inverted index when n = 2
    # dic3 stores the inverted index when n = 3
    # result is a list that stored the whole inverted list. result = [dic1, dic2, dic3]
    result = []
    dic1 = {}
    dic2 = {}
    dic3 = {}
    # for every document, read the txt file and count the word
    for docid in filedic:
        # opening the corresponding txt file according to the docid
        file = open(filedic[docid] + ".txt", "r")
        text = file.readlines()
        i = 1
        # n-gram, when n = 1, 2, 3
        while i < 4:
            if i == 1:
                dic1 = index(dic1, 1, text, docid)
            if i == 2:
                dic2 = index(dic2, 2, text, docid)
            if i == 3:
                dic3 = index(dic3, 3, text, docid)
            i = i + 1
    # write the inverted list in txt files and add them to the final result
    result.append(dic1)
    fo = open("1.txt", "w+")
    fo.write(str(dic1))
    fo.close()
    result.append(dic2)
    fo = open("2.txt", "w+")
    fo.write(str(dic2))
    fo.close()
    result.append(dic3)
    fo = open("3.txt", "w+")
    fo.write(str(dic3))
    fo.close()
    return result

# the input is the text file's docdis(docid) and its corresponding text(text),
# the n of n-gram(n), and write the result to a dictionary(dicn)
def index(dicn, n, text, docid):
    print "dealing n = " + str(n)
    if len(text) < 1:
        return dicn
    # cut the text differently according to different n of n-gram
    words = ngram(text[0], n)
    for term in words:
        if len(term) < 1:
            continue
        # for every term in the textfile, check if the term exists in the inverted index
        if dicn.has_key(term):
            # check if the docid exist
            if dicn[term].has_key(docid):
                dicn[term][docid] = dicn[term][docid] + 1
            # the docid not exist
            else:
                dicn[term][docid] = 1
        else:
            dictemp = {}
            dictemp[docid] = 1
            dicn[term] = dictemp
    return dicn

# the function cut the text(input variable input) into unigrams, bigrams, trigrams according to input n
# returns the list of term
def ngram(input, n):
    if n == 1:
        words = str(input).split()
        return words
    if n == 2:
        words = input.split()
        i = 0
        newword = []
        while i < len(words) - 1:
            newword.append(words[i] + " " + words[i + 1])
            i = i + 1
        return newword
    if n == 3:
        words = input.split()
        i = 0
        newword = []
        while i < len(words) - 2:
            newword.append(words[i] + " " + words[i + 1] + " " + words[i + 2])
            i = i + 1
        return newword

# task 3.1
# the input dic is in following format: {term1 : {docid1: termfrequency, docid2: tf2}, term2: {docid2: tf3}}
# the function will return a list called result in the format of [('term1', tf1), ('term2', tf2)]
def sortfruquent(dic):
    result = []
    for term in dic:
        counter = 0;
        for docid in dic[term]:
            counter = counter + dic[term][docid]
        result.append((term, counter))
    result.sort(key=lambda x: x[1], reverse=True)
    return result

# task 3.2
# the function will take the same input as task3.1
# the function will return a list in the format of [('term1', [doc1, doc2], df1), ('term2', [doc5], df2)]
def sortterm(dic):
    list = []
    for term in dic:
        doclist = []
        counter = 0
        for docid in dic[term]:
            doclist.append(docid)
            counter = counter + 1
        list.append((term, doclist, counter))
    return sorted(list)

# input is the result of task3, and the function will write the correspond txt file
def writeresult(result, filename):
    fo = open(filename + ".txt", "w+")
    for stuff in result:
        fo.write(str(stuff))
        fo.write('\n')
    fo.close()

# Task1
fo = open("pro1.txt", "r")
urls = fo.readlines()
i = 1
filedic = {}
for url in urls:
    print "deal doc:" + str(i)
    content(url, i, filedic)
    i = i + 1
print "begin part 2"
# Task2
result = invertedindex(filedic)
# Task3
sol31a = sortfruquent(result[0])
writeresult(sol31a, 'task3-1a')
sol32a = sortfruquent(result[1])
writeresult(sol32a, 'task3-2a')
sol33a = sortfruquent(result[2])
writeresult(sol33a, 'task3-3a')
sol31b = sortterm(result[0])
writeresult(sol31b, 'task3-1b')
sol32b = sortterm(result[1])
writeresult(sol32b, 'task3-2b')
sol33b = sortterm(result[2])
writeresult(sol33b, 'task3-3b')