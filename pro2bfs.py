import time
import requests
from bs4 import BeautifulSoup

# the seed url
url = "https://en.wikipedia.org/wiki/Sustainable_energy"
# urls is a list of urls that needs to be crawled
urls = [url]
# crawled keep all the urls which were crawled from another url in order to deduplite
clowled = [url]
# the number of crawled urls
cnumber = 1
# layer number
lnumber = 1
# remember the number of each layer, when the counter == 0, lay++
counter = 1

# open a new txt file to keep the crawled urls
fo = open("pro2bfs.txt", "wb")
fo.write(url + "\n")

# if the layer is less than 5 and the crawled urls is less than 1000 and there exist url that can be crawled
while lnumber <= 5 and len(clowled) <= 1000 and len(urls) > 0:
    try:
#        print len(urls)
        # get the first url in the list
        r = requests.get(urls[0])
        # respect the politeness policy
        time.sleep(1)
        soup = BeautifulSoup(r.content)
        urls.pop(0)
        # take the crawled url out of the list and counter--
        counter = counter - 1
    except:
        urls.pop(0)
        counter = counter - 1
        continue

    if counter <= 0:
        # when the counter decreased to 0, it will initialized as the number of urls of the next layer
        counter = len(urls)
        lnumber = lnumber + 1

    for paragraph in soup.find_all("p"):
        for link in paragraph.find_all("a"):
            # find all <a> tag that has the word "solar" in it
            if ("solar" in str(link) or "Solar" in str(link))and "#" not in str(link):
                link = "https://en.wikipedia.org" + link['href']
                # prevent duplicate
                if link not in clowled:
                    fo.write(str(link) + "\n")
                    urls.append(link)
                    clowled.append(link)
                    cnumber = cnumber + 1
#                    print "layernumber: " + str(lnumber)

print len(clowled)
print clowled
fo.close()