import time
import requests
from bs4 import BeautifulSoup

#url is the seed url
url = "https://en.wikipedia.org/wiki/Sustainable_energy"
#urls is a list of urls that needs to be crawled
urls = [url]
#crawled keep all the urls that was crawled from another url
crawled = [url]
# the number of crawled urls
cnumber = 1
# layer number
lnumber = 1
# counter counts the number of urls of each layer, when the counter == 0, lay++
counter = 1

# open a new txt file to keep the crawled urls
fo = open("pro1.txt", "wb")
fo.write(url + "\n")

# if the layer is less than 5 and the crawled urls is less than 1000
while lnumber <= 5 and len(crawled) <= 1000:
    # get the first url in the list
    r = requests.get(urls[0])
    # respect the politeness policy
    time.sleep(1)
    soup = BeautifulSoup(r.content)
    # take the crawled url out of the list and counter--
    urls.pop(0)
    counter = counter - 1

    # when the counter decreased to 0, it will initialized as the number of urls of the next layer, than the number of layer add 1
    if counter <= 0:
        counter = len(urls)
        lnumber = lnumber + 1

    for paragraph in soup.find_all("p"):
        for link in paragraph.find_all("a", href = True):
            # deal with the # situation of the url
            if "#" not in str(link):
                link = "https://en.wikipedia.org" + link['href']
                # duplicate remove in order not to crawl the same url more than one time
                if link not in crawled:
                    # write the new url in the txt file
                    fo.write(link + "\n")
                    # add the new url list to be crawled in the future
                    urls.append(link)
                    # add it to the crawled list
                    crawled.append(link)
                    cnumber = cnumber + 1
            if "#" in str(link):
                if len(link['href'].split('#')[0] ) != 0:
                    link = "https://en.wikipedia.org" + link['href']
                    link = str(link).split('#')[0]
                    if link not in crawled:
                        fo.write(link + "\n")
                        urls.append(link)
                        crawled.append(link)
                        cnumber = cnumber + 1

print crawled
fo.close()