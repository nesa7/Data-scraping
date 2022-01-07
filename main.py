import pandas as pd
from importlib import import_module

def main():
    sites = get_sites()
    sitesData = []

    for index, site in sites.iterrows():
        link = site["link"]
        id = site["id"]

        try:
            siteScraper = get_scraper(id)

        except:
            print("No class for site with id: " + id)

        siteData = siteScraper.scrape(link)
        sitesData.extend(siteData)

    colNames = ['State','County','Name','Address','Hours']
    outData = pd.DataFrame(sitesData, columns = colNames)
    outData.to_excel("tester.xlsx", encoding ='utf-8')

def get_sites():
    return pd.read_excel("sites.xlsx")

def get_scraper(id):
    return getattr(import_module("scrapers."+id), id)()

main()

