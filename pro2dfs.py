# I used to recursion to accomplish dfs
import time
import requests
from bs4 import BeautifulSoup

# the function need 3 variables, url is the hyperlink that needs to be crawled, layer is the number of depth
# visited is a list that keep all the hyperlinks that already been found in order to prevent duplicate
def dfs(url, layer, visited):
    # If the layer is deeper than 5 or the crawled urls is more than 1000, return the solution
    if layer <= 5 and len(visited) <= 1000:
#        print "layer: " + str(layer)
        r = requests.get(url)
        # respect the politeness policy
        time.sleep(1)
        soup = BeautifulSoup(r.content)
        for paragraph in soup.find_all("p"):
            for link in paragraph.find_all("a", href = True):
                try:
                    # find all the hyperlinks that contains the keyword "solar"
                    if ("solar" in str(link) or "Solar" in str(link)) and len(visited) <= 1000 and "#" not in str(link):
                        linkpass = "https://en.wikipedia.org" + link['href']
                        if linkpass not in visited:
                            # add the url to prevent duplicate
                            visited.append(linkpass)
#                            print link['href']
#                            print "visitedlength: " + str(len(visited))
                            # keep crawling the next layer
                            dfs(linkpass, layer + 1, visited)
                except:
                    continue
    return visited


url = "https://en.wikipedia.org/wiki/Sustainable_energy"
visited = [url]

fo = open("pro2dfs.txt", "wb")
dfs(url, 1, visited)
print visited
# write the result to a txt file
for item in visited:
    fo.write(item + "\n")
fo.close()
