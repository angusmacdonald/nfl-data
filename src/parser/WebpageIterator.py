import DataParser
import GetData

def getNflData(urlPrefix):

	startYear = 1995
	endYear = 2015

	for year in range(startYear, endYear):

		fullUrl = "{}{}/".format(urlPrefix, year)
		print "Extracting data from " + fullUrl

		tmpDest = "data/{}.tmp".format(year)
		print "Saving temporary results to " + tmpDest

		resultDest = "results/{}.csv".format(year)
		print "Saving results to " + resultDest

		GetData.downloadWebpage(fullUrl, tmpDest)
		DataParser.parseTableToCSV(tmpDest, resultDest)


if __name__ == '__main__':
	getNflData("http://www.sportingcharts.com/nfl/stats/yards-after-the-catch/")