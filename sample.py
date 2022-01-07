from bs4 import BeautifulSoup
import pandas as pd
import mechanicalsoup
import sites
from sites import *
import glob
import re
from sites import scraper

def main():
    sites = get_sites()
    sitesData = []
    print(sites)
    for index, site in sites.iterrows():
        link = site["link"]
        id = site["id"]

        siteScraper = scraper.scraper_factory[id]()
        siteData = siteScraper.scrape(link)
        sitesData.extend(siteData)

    fileOut = "samppo"
    colNames = ['State','County','Name','Address','Hours']
    outData = pd.DataFrame(sitesData, columns = colNames)
    outData.to_excel(fileOut + ".xlsx", encoding ='utf-8')

def get_sites():
    return pd.read_excel("sites.xlsx")

main()

