from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import pandas as pd
import mechanicalsoup
import glob
import re

class scraper(ABC):

    @abstractmethod
    def scrape():
        pass

class salvArmy(scraper):

    def scrape(self, link: str):
        
        browser = mechanicalsoup.Browser()
        page = browser.get(link)
        soup = BeautifulSoup(page.content, "html5lib")
        matches = soup.find_all('div', class_='content')
        centersList = []
    
        for tag in matches:
            try:

                listing = []
                #address = soup.find('p')
                tagList = tag.text.splitlines()
                # state
                pattern = r'[0-9]'
                cleanState = tagList[4].split(',', 1)[1]
                cleanState = re.sub(pattern, '', cleanState)
                listing.append(cleanState)

                # county
                cleanCounty = tagList[4].split(',', 1)[0]
                cleanCounty = re.sub(r"[\t]*", "", cleanCounty)
                listing.append(cleanCounty)

                # name
                cleanName = re.sub(r"[\t]*", "", tagList[2])
                listing.append(cleanName)

                # address
                cleanAddress = re.sub(r"[\t]*", "", tagList[3])
                listing.append(cleanAddress)

                # Hours
                cleanHours = re.sub(r"[\t]*", "", tagList[6])
                listing.append(cleanHours)
                if len(listing) == 5:
                    centersList.append(listing)
            except:
                pass

        return centersList


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


scraper_factory = {
    'salvArmy': salvArmy,
    'NJ': NJ
}