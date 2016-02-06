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

	# Delete any existing results file:
	deleteFileIfExists(resultsFileName)

	soup = BeautifulSoup(content, "lxml")

	# Find the table element, then iterate over entries:
	table = soup.find("table")

	# Information to append to line
	headerToAppend = ", Year"
	dataToAppend = ", {}".format(year)

	# Write header then data to results file:
	writeTdEntriesToFile(resultsFileName, table.findAll("tr"), "th", headerToAppend)
	writeTdEntriesToFile(resultsFileName, table.findAll("tr"), "td", dataToAppend)

"""
Iterate over all td elements in every table row (tr), and write
as CSV to the results file.

Args:
	resultsFileName (str): where data is written 
	rows: BeautifulSoup rows
	entryMarker: what an entry in the row is identified as (td or th)
	strToAppend (str): string to add to end of each line

"""
def writeTdEntriesToFile(resultsFileName, rows, entryMarker, strToAppend):
	data = [[td.findChildren(text=True) for td in tr.findAll(entryMarker)] for tr in rows]

	# Write entries to disk, comma separated:
	with open(resultsFileName, "a") as results:
		for row in data:
			if (len(row) > 0):
				results.write(", ".join([str(x[0]) for x in row]))
				results.write(strToAppend)
				results.write("\n")

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
