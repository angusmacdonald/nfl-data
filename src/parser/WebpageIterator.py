import DataParser
import GetData

import os

def getNflData(urlPrefix, startYear, endYear):

	createRequiredDirectories(["data", "results"])

	for year in range(startYear, endYear):

		fullUrl = "{}{}/".format(urlPrefix, year)
		print "Extracting data from " + fullUrl

		tmpDest = "data/{}.tmp".format(year)
		print "Saving temporary results to " + tmpDest

		resultDest = "results/{}.csv".format(year)
		print "Saving results to " + resultDest

		GetData.downloadWebpage(fullUrl, tmpDest)
		DataParser.parseTableToCSV(tmpDest, resultDest, year)

		deleteFileIfExists(tmpDest)

def createRequiredDirectories(dirs):
	for dir in dirs:
		if not os.path.exists(dir):
			os.makedirs(dir)


def deleteFileIfExists(filename):
	try:
		os.remove(filename)
	except OSError:
		pass

if __name__ == '__main__':
	getNflData("http://www.sportingcharts.com/nfl/stats/yards-after-the-catch/", 1995, 2016)