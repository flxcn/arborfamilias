import requests
from bs4 import BeautifulSoup
from treelib import Node, Tree

# initialize empty list of family members
# familia = []
familia = Tree()
existing_personae = set()
print("Enter the URL of your base article:")
base_article_url = input()

# recursive function to scrape a Wikipedia article
def findChildren(url,generation,parent_article):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find(id="firstHeading")

    if url not in existing_personae:
        print(title.text)
        existing_personae.add(url)

        if parent_article == "":
            familia.create_node(title.text, url)
        else:
            familia.create_node(title.text, url, parent=parent_article)

        infoboxLabels = soup.find_all('th',{"class":"infobox-label"})
        for label in infoboxLabels:
            # matches = ["Children", "Issue"]
            # if any(x in label.text for x in matches):
            if "Issue" in label.text:
                children = []
                children = label.find_next("td").find_all("a")
                for child in children:
                    # check to ensure only Wikipedia links are followed
                    if child['href'].find("/wiki/") == -1: 
                        continue

                    # go forward one more generation
                    gen = generation
                    gen += 1
                    findChildren("https://en.wikipedia.org" + child['href'], gen, url)
                break 

# "https://en.wikipedia.org/wiki/William_Rockefeller_Sr."
findChildren(base_article_url, 0,"")

familia.show()
# print(familia.depth())
# familia.save2file("familia.txt")
# jsonFile = open('familia.json', 'w')
# jsonFile.write(familia.to_json(with_data=True))
# jsonFile.close()
# for persona in familia:
#     print(persona)