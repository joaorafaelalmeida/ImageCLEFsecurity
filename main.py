import os
import argparse

JPG_MN = "FF D8 FF DB"
GIF_MN = "47 49 46 38 37 61"
PDF_MN = "25 50 44 46 2d"
PNG_MN = "89 50 4E 47 0D 0A 1A 0A"

def convertFiles(dir, standardFile):
	# read all the files
	# read the right format from the file
	# change the file name
	# change the magic numbers
	# store in a new dir
	pass

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--convert", help="Convert files to original format", action="store_true")
	args = parser.parse_args()

	if args.convert:
		print "Convert files to original format"
		convertFiles(".","goldStandard")


if __name__ == "__main__":
   main()