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
	cursor = receiving.find( { "$and": [ { "Team": team }, { "Year": year } ] } )

	result = []

	totalReceptionNumbers = 0
	totalYards = 0

	for player in cursor:
		totalReceptionNumbers += player['Rec']
		totalYards += player['Rec Yards']

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

		playerRes['width'] = (player['Rec'] / float(totalReceptionNumbers)) * 100
 		playerRes['label'] = str(player['Player'])

 		height = ((player['Rec Yards'] / float(totalYards)) * 100) * 2
 		
 		percentageYac = min (1, player['YAC'] / float(player['Rec Yards']))
 		percentageNonYac = 1- percentageYac

		print percentageNonYac
 		sliceNonYac = {}

 		sliceNonYac['height'] = height * percentageNonYac
 		sliceNonYac['color'] = "#4AE85D"
 		sliceNonYac['label'] = "{} yards in air".format(max(0, player['Rec Yards']-player['YAC']))

 		sliceYac = {}

 		sliceYac['height'] = height * percentageYac
 		sliceYac['color'] = "#20D635"
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

