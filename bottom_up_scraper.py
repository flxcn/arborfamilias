import requests
from bs4 import BeautifulSoup
from treelib import Node, Tree

# initialize empty list of family members
familia = Tree()
existing_personae = set()
print("Enter the URL of your base article:")
base_article_url = input()

# recursive function to scrape a Wikipedia article
def findParents(url,generation,child_article):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find(id="firstHeading")

    # familia.append(title.text + ", Generation:" + str(generation))

    if url not in existing_personae:
        print(title.text)
        existing_personae.add(url)

        if child_article == "":
            familia.create_node(title.text,url)
        else:
            familia.create_node(title.text,url, parent=child_article)

        infoboxLabels = soup.find_all('th',{"class":"infobox-label"})
        for label in infoboxLabels:

            if "Father" in label.text:
                fathers = []
                fathers = label.find_next().find_all("a")
                for father in fathers:
                    # check to ensure only Wikipedia links are followed
                    if father['href'].find("/wiki/") == -1: 
                        continue

                    # check to prevent duplicate entries, which may cause an infinite loop
                    if any(father.text in s for s in existing_personae):
                        continue

                    # go up one more generation
                    gen = generation
                    gen -= 1
                    findParents("https://en.wikipedia.org" + father['href'], gen, url)

            if "Mother" in label.text:
                mothers = []
                mothers = label.find_next().find_all("a")
                for mother in mothers:
                    # check to ensure only Wikipedia links are followed
                    if mother['href'].find("/wiki/") == -1: 
                        continue

                    # check to prevent duplicate entries, which may cause an infinite loop
                    if any(mother.text in s for s in existing_personae):
                        continue

                    # go up one more generation
                    gen = generation
                    gen -= 1
                    findParents("https://en.wikipedia.org" + mother['href'], gen, url)
                
    
findParents(base_article_url, 0, "")

familia.show()
# # print out each family member
# for persona in familia:
#     print(persona)