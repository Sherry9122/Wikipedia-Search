import time
import requests
from bs4 import BeautifulSoup

fo = open("pro1.txt", "r")
i = 10

url = fo.readlines()


for tempurl in url:
    print tempurl,"\n"
    # get the url
    tempurl = str(tempurl).split("\n")[0]
    try:
        # store 1000 files
        if i > 1000:
            exit()

        r = requests.get(tempurl).text
        print r
        # respect the politeness policy
        time.sleep(1)
        # create a new file named i.txt
        name = str(i) + ".txt"
        fnew = open(name, "w")
        sour = unicode(r).encode('utf8')
        fnew.write(sour)
        fnew.close()
        i = i + 1
        print i,"\n"
    except:
        continue

