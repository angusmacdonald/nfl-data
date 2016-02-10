from lxml import html
from bs4 import BeautifulSoup
import requests
import sys
import os

"""
Parse the table tag in the provided file into a CSV file
"""
def parseTableToCSV(inputFilename, resultsFileName, year):

	# Read content of file into memory, removing new lines:
	with open (inputFilename) as datafile:
		content = datafile.read().replace('\n', '')

	soup = BeautifulSoup(content, "lxml")

	# Find the table element, then iterate over entries:
	table = soup.find("table")

	# Information to append to line
	headerToAppend = ", YEAR"
	dataToAppend = ", {}".format(year)

	# Write header then data to results file:
	
	entriesParsed = writeTdEntriesToFile(resultsFileName, table.findAll("tr"), "td", dataToAppend, headerToAppend)

	return entriesParsed


"""
Iterate over all td elements in every table row (tr), and write
as CSV to the results file.

Args:
	resultsFileName (str): where data is written 
	rows: BeautifulSoup rows
	entryMarker: what an entry in the row is identified as (td or th)
	strToAppend (str): string to add to end of each line
	headerToAppend (str): string to add to the end of the header (first) line

Return:
	The number of entries parsed on this page.
"""
def writeTdEntriesToFile(resultsFileName, rows, entryMarker, strToAppend, headerToAppend):
	data = [[td.findChildren(text=True) for td in tr.findAll(entryMarker)] for tr in rows]

	entriesParsed = 0

	firstRow = True
	valToAppend = headerToAppend

	# Write entries to disk, comma separated:
	with open(resultsFileName, "a") as results:
		for row in data:
			if (len(row) > 0):
				
				if (str(row[1][0]) != "PLAYER" or firstRow): # Ignore the header format
					results.write(", ".join([x[0].encode('utf-8').replace(",", "") for x in row[1:20]]))
					results.write(valToAppend)
					results.write("\n")

					if firstRow:
						firstRow = False
						valToAppend = strToAppend
					else:
						entriesParsed += 1			

	return entriesParsed


def deleteFileIfExists(filename):
	try:
		os.remove(filename)
	except OSError:
		pass


"""
Arguments:
 1st: Source file
 2nd: Destination CSV
"""
if __name__ == '__main__':
	inputFilename = sys.argv[1]
	resultsFileName = sys.argv[2]

	parseTableToCSV(inputFilename, resultsFileName, "N/A")
