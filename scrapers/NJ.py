from bs4 import BeautifulSoup
import mechanicalsoup
import re
from .scraperFactory import scraper

class NJ(scraper):

    def __init__(self):
        self.stopwords = ["Directions", "Open:", "counties", "served:", "Location",]

    def scrape(self, link: str):
        stateName = 'New Jersey'
        browser = mechanicalsoup.Browser()
        page = browser.get(link)
        #paginatorLinks = page.soup.find_all(class_ = "filtered-list__item")
        soup = BeautifulSoup(page.content, "html5lib")

        centersList = []

        results = soup.find_all(class_="filtered-list__item")
        for tag in results:
            tListing = []
            tListing.append(stateName)

            tCounty = tag.find(class_="node__counties")
            if tCounty is not None:
                tCounty = self.cleanString(tCounty.text)
            tListing.append(tCounty)

            tName = tag.find(href=re.compile("/center/"))
            if tName is not None:
                tName = self.cleanString(tName.text)
            tListing.append(tName)

            tAddress = tag.find(class_="node__location")
            if tAddress is not None:
                tAddress = self.cleanString(tAddress.text)
            tListing.append(tAddress)

            tHours = tag.find(class_="node__hours")
            if tHours is not None:
                tHours = self.cleanString(tHours.text)
            tListing.append(tHours)

            if len(tListing) == 5:
                centersList.append(tListing)
        
        return centersList

    def cleanString(self, uncleanStr):
        tokens = uncleanStr.split()
        cleanTokens = [t for t in tokens if not t in self.stopwords]
        cleanText = " ".join(cleanTokens)
        clean_text = re.sub(r"[^A-Za-z0-9\s]+", "", cleanText)
        return cleanText