from bs4 import BeautifulSoup
import pandas as pd
import mechanicalsoup
import sites
from sites import *
import glob
import re
import scraper

def main():
    sites = get_sites()
    sitesData = []

    for index, site in sites.iterrows():
        link = site["link"]
        id = site["id"]

        try:
            siteScraper = scraper.scraper_factory[id]()
        except:
            print("No class for site with id: " + id)
        siteData = siteScraper.scrape(link)
        sitesData.extend(siteData)

    fileOut = "tester"
    colNames = ['State','County','Name','Address','Hours']
    outData = pd.DataFrame(sitesData, columns = colNames)
    outData.to_excel(fileOut + ".xlsx", encoding ='utf-8')

def get_sites():
    return pd.read_excel("sites.xlsx", nrows=2)

main()

