import requests
from bs4 import BeautifulSoup

# initialize empty list of family members
familia = []

# recursive function to scrape a Wikipedia article
def scrapeWikiArticle(url,generation):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find(id="firstHeading")

    familia.append(title.text + ", Generation:" + str(generation))

    infoboxLabels = soup.find_all('th',{"class":"infobox-label"})
    for label in infoboxLabels:
        if "Issue" in label.text:
            children = label.find_next().find_all("a")
            for child in children:
                # check to ensure only Wikipedia links are followed
                if child['href'].find("en.wikipedia.org/wiki/") == -1: 
                    continue

                # check to prevent duplicate entries, which may cause an infinite loop
                if any(child.text in s for s in familia):
                    continue

                # go forward one more generation
                gen = generation
                gen += 1
                scrapeWikiArticle("https://en.wikipedia.org" + child['href'], gen)
            break 


scrapeWikiArticle("https://en.wikipedia.org/wiki/Augustus", 1)

for persona in familia:
    print(persona)