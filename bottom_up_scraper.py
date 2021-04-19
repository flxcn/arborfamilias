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

        if "Father" in label.text:
            fathers = label.find_next().find_all("a")
            for father in fathers:
                # check to ensure only Wikipedia links are followed
                if father['href'].find("/wiki/") == -1: 
                    continue

                # check to prevent duplicate entries, which may cause an infinite loop
                if any(father.text in s for s in familia):
                    continue

                # go up one more generation
                gen = generation
                gen -= 1
                scrapeWikiArticle("https://en.wikipedia.org" + father['href'], gen)

        if "Mother" in label.text:
            mothers = label.find_next().find_all("a")
            for mother in mothers:
                # check to ensure only Wikipedia links are followed
                if mother['href'].find("/wiki/") == -1: 
                    continue

                # check to prevent duplicate entries, which may cause an infinite loop
                if any(mother.text in s for s in familia):
                    continue

                # go up one more generation
                gen = generation
                gen -= 1
                scrapeWikiArticle("https://en.wikipedia.org" + mother['href'], gen)
                
    
scrapeWikiArticle("https://en.wikipedia.org/wiki/Nero", 0)

# print out each family member
for persona in familia:
    print(persona)