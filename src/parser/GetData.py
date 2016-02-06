import urllib
import sys

"""
Download the contents of a webpage, saving it
to the given file location.
"""
def downloadWebpage(srcUrl, destFile):

	print "Downloading content of " + srcUrl

	f = urllib.urlopen(srcUrl)
	pagedata = f.read()

	with open(destFile, "w") as results:
		results.write(pagedata)

	print "Saved content to " + destFile

"""
Arguments:
 1st: Source webpage
 2nd: Destination file
"""
if __name__ == '__main__':
	srcUrl = sys.argv[1]
	destFile = sys.argv[2]

	downloadWebpage(srcUrl, destFile)