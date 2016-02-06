from lxml import html
from bs4 import BeautifulSoup
import requests
import sys

"""
Parse the table tag in the provided file into a CSV file
"""
def parseTableToCSV(inputFilename, resultsFileName):
	
	# Read content of file into memory, removing new lines:
	with open (inputFilename) as datafile:
		content = datafile.read().replace('\n', '')

	soup = BeautifulSoup(content)

	# Find the table element, then iterate over entries:
	table = soup.find("table")
	rows = table.findAll("tr")

	data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]

	# Write entries to disk, comma separated:
	with open(resultsFileName, "a") as results:
		for row in data:
			results.write(", ".join([str(x[0]) for x in row]))	
			results.write("\n")

"""
Arguments:
 1st: Source file
 2nd: Destination CSV
"""
if __name__ == '__main__':
	inputFilename = sys.argv[1]
	resultsFileName = sys.argv[2]
