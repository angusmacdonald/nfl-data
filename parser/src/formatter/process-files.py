import PIL

import sys

img = PIL.Image.open('img.jpg')
exif_data = img._getexif()

def saveOutputAsJson(output, fileName):
	json_data = json.dumps(output, sort_keys=True, indent=4, separators=(',', ': '))

	with open(fileName, "w") as text_file:
		text_file.write(json_data)


if __name__ == '__main__':
	databaseName = sys.argv[1]
	collectionName = sys.argv[2]