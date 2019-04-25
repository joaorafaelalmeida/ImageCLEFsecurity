import os
import argparse
import pathlib
import binascii
import logging as lg
from os import listdir
from os.path import isfile, join
import JPGrules
import operator

def setup_logger(name, log_file, level=lg.INFO):
	formatter = lg.Formatter('%(asctime)s %(message)s', datefmt='%d/%m/%y %I:%M:%S %p')
	handler = lg.FileHandler(log_file)
	handler.setFormatter(formatter)		
	logger = lg.getLogger(name)

	if logger.handlers:
		logger.handlers[0].close()
		logger.handlers = []

	logger.setLevel(level)
	logger.addHandler(handler)

	return logger

def readFileInHEX(filename):
	with open(filename, 'rb') as f:
		content = f.read()
	return binascii.hexlify(content)

def processFiles(dir):
	allFiles = [f for f in listdir(dir) if isfile(join(dir, f))]
	allScores = {}
	for file in allFiles:
		fileInProcess = readFileInHEX(dir+"/"+file)
		score = {}
		score["jpg"] = JPGrules.isJPG(fileInProcess)
		#...
		fileType = sorted(score.items(), key=operator.itemgetter(1))[0][0]
		#Structure is: file:(type, {scores..})
		allScores[file] = (fileType, score)
	return allScores

def writeResult(allScores, resultFile, writeScore=False):
	f = open(resultFile, "w")
	for score in allScores:
		result = score + ";" + allScores[score][0]
		if writeScore:
			result += ";" + str(allScores[score][1])
		f.write(result+"\n")
	f.close()

def calculateGlobalScore(allScores, groundtruth):
	detectedAlteredImages=-1
	totalDetectionsAlteredImages=-1
	totalAlteredImages=-1

	precision=detectedAlteredImages/totalDetectionsAlteredImages
	recall=detectedAlteredImages/totalAlteredImages
	fMeasure=2*(precision*recall)/(precision+recall)

	print("\n\n+ + + Scores + + +\n\n")
	print("Precision: " + str(precision))
	print("Recall: " + str(recall))
	print("F-Measure: " + str(fMeasure))


def main():
	pathlib.Path('logs').mkdir(parents=True, exist_ok=True)
	pathlib.Path('results').mkdir(parents=True, exist_ok=True)
	er_logger = setup_logger('error_log', 'logs/error.log')

	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--convert", help="Convert files to original format", action="store_true")
	parser.add_argument("-fh", "--file-to-hexa",  dest='filetohexa', type=str, default="",\
					help="Read and print file in hexadecimal format")
	
	parser.add_argument("-p", "--process", help="Process the files and compare with the ground truth", action="store_true")
	parser.add_argument("-ss", "--show-individual-scores", dest='showindividualscores', \
					help="Add a new field with in the result file with the scores", action="store_true")
	
	parser.add_argument("-d", "--dir-of-files",  dest='filesdir', type=str, default="T1DataSet",\
					help="Directory with files to process (Default: T1DataSet)")	
	parser.add_argument("-rf", "--result-file",  dest='resultfile', type=str, default="results/task1.txt",\
					help="Result file with the classification of each file (Default: results/task1.txt)")
	parser.add_argument("-gt", "--ground-truth",  dest='groundtruth', type=str, \
					default="GroundTruthDataSet/ground_truth_training_set_task_1.txt",\
					help="Ground truth text file (Default: GroundTruthDataSet/ground_truth_training_set_task_1.txt)")
	args = parser.parse_args()

	if args.convert:
		print ("Convert files to original format")
		print ("TO DO")

	if args.filetohexa != "":
		print ("Print file in hexadecimal\n\n")
		print (readFileInHEX(args.filetohexa))

	if args.process:
		print ("Process files...\n\n")
		allScores = processFiles(args.filesdir)
		writeResult(allScores, args.resultfile, args.showindividualscores)
		calculateGlobalScore(allScores, args.groundtruth)

if __name__ == "__main__":
   main()