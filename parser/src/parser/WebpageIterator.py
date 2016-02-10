import DataParser
import GetData

import os

def getNflData(initUrl, startYear, endYear):

	createRequiredDirectories(["data", "results"])

	for year in range(startYear, endYear):


		resultDest = "results/{}.csv".format(year)
		print "Saving results to " + resultDest
		# Delete any existing results file:
		deleteFileIfExists(resultDest)
		

		count = 1

		numCounted = 1 # > 0 to start loop


		while numCounted > 0:

			fullUrl = initUrl.format(year, count)
			print "Extracting data from " + fullUrl

			tmpDest = "data/{}-{}.tmp".format(year, count)
			print "Saving temporary results to " + tmpDest

			GetData.downloadWebpage(fullUrl, tmpDest)
			numCounted = DataParser.parseTableToCSV(tmpDest, resultDest, year)

			count += numCounted

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
	startYear = 2006 # first year of YAC being recorded on ESPN
	endYear = 2015
	getNflData("http://espn.go.com/nfl/statistics/player/_/stat/receiving/sort/receivingYardsAfterCatch/year/{}/seasontype/2/qualified/false/count/{}", startYear, endYear+1)