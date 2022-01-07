import re
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import mechanicalsoup

fileOut = "NJ Sample Set2"
baseURL = "https://web.archive.org/web/20210701183644/https://www.nj211.org/nj-cooling-centers"
column_names = ['State','County','Name','Address','Hours']
stateName = 'New Jersey'
countyName = ''
centerName = ''
centerAddress = ''
centerHours = ''
centersList = []

stopwords = ["Directions", "Open:", "counties", "served:", "Location",]

def cleanString(uncleanStr):
	tokens = uncleanStr.split()
	cleanTokens = [t for t in tokens if not t in stopwords]
	cleanText = " ".join(cleanTokens)
	clean_text = re.sub(r"[^A-Za-z0-9\s]+", "", cleanText)
	return cleanText

def createCSV(dataSet):
	outData = pd.DataFrame(dataSet, columns = column_names)
	outData.to_csv(fileOut + ".csv")

def main():
	browser = mechanicalsoup.Browser()
	page = browser.get(baseURL)
	#paginatorLinks = page.soup.find_all(class_ = "filtered-list__item")
	soup = BeautifulSoup(page.content, "html5lib")
	results = soup.find_all(class_="filtered-list__item")
	for tag in results:
		tListing = []
		tListing.append(stateName)

		tCounty = tag.find(class_="node__counties")
		if tCounty is not None:
			tCounty = cleanString(tCounty.text)
		tListing.append(tCounty)
			
		tName = tag.find(href=re.compile("/center/"))
		if tName is not None:
			tName = cleanString(tName.text)
		tListing.append(tName)
			
		tAddress = tag.find(class_="node__location")
		print(tAddress)
		if tAddress is not None:
			tAddress = cleanString(tAddress.text)
		tListing.append(tAddress)
		
		tHours = tag.find(class_="node__hours")
		if tHours is not None:
			tHours = cleanString(tHours.text)
		tListing.append(tHours)
		centersList.append(tListing)
	
	createCSV(centersList)
	print("DONE")
		
main()
