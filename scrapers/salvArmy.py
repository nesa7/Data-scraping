from bs4 import BeautifulSoup
import mechanicalsoup
import re
from .scraperFactory import scraper

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
