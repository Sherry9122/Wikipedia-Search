import time
import requests
from bs4 import BeautifulSoup

def managefile():
    fo = open("pro1.txt", "r")
    dic = {}
    urls = fo.readlines()
    for url in urls:
        try:
            processtest(dic, url)
        except:
            continue
    print dic
    return dic

def processtest(dic, url):
    # get docid
    docid = url.split('/')
    docid = docid[len(docid) - 1]
    docid = docid.split('\n')[0]
    if len(docid) > 0:
        print docid
        tempurl = url.split('\n')[0]
        print tempurl
        dic[docid] = tempurl
    return dic

def crawling(dic):
    result = {}
    for key in dic:
        result[key] = []
    for key in dic:
        try:
            url = dic[key]
            r = requests.get(url)
            time.sleep(1)
            soup = BeautifulSoup(r.content)
            print "now crawling :" + str(url)
            for paragraph in soup.find_all("p"):
                # extract all the links in the page
                for link in paragraph.find_all("a", href=True):
                    # deal with the # situation of the url
                    if "#" not in str(link) and len(link) > 0:
                        link = processlink(link)
                        print "extract the docid: " + link
                        # extract the doc id, if the docid that the link points to is in a graph
                        if result.has_key(link):
                            # if there exists links that point to the docid, add the new docid to the hash map value, which is a list
                            if key not in result[link]:
                                print "writing dic"
                                result[link].append(key)
                            # if there is no links to the new docid, create a key value pair and add them in the doc
        except:
            continue
    return result

def writeresult(result):
    fo = open("G1.txt", "wb")
    for key in result:
        fo.write(str(key) + ' ')
        for docid in result[key]:
            fo.write(str(docid) + ' ')
        fo.write('\n')
    print result

def processlink(link):
    link = link['href']
    link = str(link)
    link = link.split('/')
    link = link[len(link) - 1]
    return str(link)

dic = managefile()
result = crawling(dic)
writeresult(result)

