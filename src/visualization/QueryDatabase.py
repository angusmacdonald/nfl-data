from pymongo import MongoClient

import sys
import json


def createSpieChartOutput(databaseName, collectionName, year):
	client = MongoClient()

	db = client[databaseName]
	receiving = db[collectionName]

	result = outputSpieChartForTeamYear(receiving, year, "GB")

	return result

def outputSpieChartForTeamYear(receiving, year, team):
	cursor = receiving.find( { "$and": [ { "TEAM": team }, { "YEAR": year } ] } )

	result = []

	totalReceptionNumbers = 0
	totalYards = 0

	for player in cursor:
		totalReceptionNumbers += player['REC']
		totalYards += player['YDS']

	print totalYards
	print totalReceptionNumbers

	cursor.rewind()


	"""
	Required format

	{
	    width: 20,
	    label: "Segment Label",
	    slices :
	        [
	            {
	                height: 300,
	                color: "#4AE85D",
	                highlight: "#55FA68",
	                label: "Slice Label 1"
	            },
	            {
	                height: 100,
	                color: "#20D635",
	                highlight: "#23FA3C",
	                label: "Slice Label 2"
	            }
	        ]
	}
	"""
	for player in cursor:

		print player

		playerRes = {}

		playerRes['width'] = (player['REC'] / float(totalReceptionNumbers)) * 100
 		playerRes['label'] = str(player['PLAYER'])

 		height = max(10, ((player['YDS'] / float(totalYards)) * 100) * 2)
 		
 		percentageYac = min (1, player['YAC'] / float(player['YDS']))
 		percentageNonYac = 1- percentageYac

		print percentageNonYac
 		sliceNonYac = {}

 		sliceNonYac['height'] = height * percentageNonYac
 		sliceNonYac['color'] = "#203731"
 		sliceNonYac['highlight'] = "#234D42"
 		sliceNonYac['label'] = "{} yards in air".format(max(0, player['YDS']-player['YAC']))

 		sliceYac = {}

 		sliceYac['height'] = height * percentageYac
 		sliceYac['color'] = "#FFB612"
 		sliceYac['highlight'] = "#F0AE1A"
 	
 		sliceYac['label'] = "{} yards after catch".format(player['YAC'])

 		playerRes['slices'] = [sliceYac, sliceNonYac]

 		result.append(playerRes)

	return result

def saveOutputAsJson(output, fileName):
	json_data = json.dumps(output, sort_keys=True, indent=4, separators=(',', ': '))

	with open(fileName, "w") as text_file:
		text_file.write(json_data)


if __name__ == '__main__':
	databaseName = sys.argv[1]
	collectionName = sys.argv[2]
	year = int(sys.argv[3])
	fileName = sys.argv[4]

	output = createSpieChartOutput(databaseName, collectionName, year)

	saveOutputAsJson(output, fileName)

