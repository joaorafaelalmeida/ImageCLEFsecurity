import os
import argparse
import pathlib
import binascii
import logging as lg
from os import listdir
from os.path import isfile, join
import JPGrules
import operator
import PNGrules
import GIFrules
import PDFrules

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
		print (file)
		score = {}
		score["jpg"] = JPGrules.isJPG(fileInProcess)
		score["png"] = PNGrules.isPNG(fileInProcess)
		score["gif"] = GIFrules.isGIF(fileInProcess)
		score["pdf"] = PDFrules.isPDF(fileInProcess)
		classification = sorted(score.items(), key=operator.itemgetter(1), reverse=True)[0]
		if(classification[1] == 0):
			fileType = "NULL"
		else:
			fileType = classification[0]
		#Structure is: file:(type, {scores..})
		allScores[file] = (fileType, score)
	return allScores

def writeResult(allScores, resultFile, writeScore=False, writeRealExtension=False, groundtruth=""):
	f = open(resultFile, "w")
	if writeRealExtension:
		groundTruthContent = readGroundTruth(groundtruth)
	for score in allScores:
		result = score + ";" + allScores[score][0]
		if writeScore:
			result += ";" + str(allScores[score][1])
		if writeRealExtension:
			matching = [s for s in groundTruthContent if score.split(".")[0] in s][0]
			result += ";" + matching.split(";")[1]
		f.write(result+"\n")
	f.close()

def calculateGlobalScore(dir, allScores, groundtruth):
	totalAlteredImages, totalImages, fail, scored = callculateAlteredImages(dir, allScores, groundtruth)
	#detectedAlteredImages=-1 
	#allDetectedAlteredImages=-1

	#precision=detectedAlteredImages/allDetectedAlteredImages
	#recall=detectedAlteredImages/totalAlteredImages
	#fMeasure=2*(precision*recall)/(precision+recall)

	print("\n\n+ + + Scores + + +\n")
	print("Total of images in directory: " + str(totalImages))
	print("Fails: " + str(fail))
	print("Scored: " + str(scored))
	print("Percentage of success: " + str((scored*100)/totalImages))
	#print("Precision: " + str(precision))
	#print("Recall: " + str(recall))
	#print("F-Measure: " + str(fMeasure))

def callculateAlteredImages(dir, allScores, groundtruth):
	alteredImages = 0
	totalImages = 0
	fail = 0
	scored = 0
	groundTruthContent = readGroundTruth(groundtruth)
	
	allFiles = [f for f in listdir(dir) if isfile(join(dir, f))]
	for file in allFiles:
		extension = file.split(".")[1]
		matching = [s for s in groundTruthContent if file.split(".")[0] in s][0]
		realExtension = matching.split(";")[1]
		if(realExtension != extension):
			alteredImages += 1
		totalImages += 1

		#Structure is: file:(type, {scores..})
		myPrevision = allScores[file][0]
		if(realExtension != myPrevision):
			fail += 1
		else:
			scored += 1
	return (alteredImages, totalImages, fail, scored)

def readGroundTruth(groundtruth):
	groundTruthContent = []
	f = open(groundtruth, "r")
	for x in f:
		groundTruthContent += [x.split("\n")[0]]
	return groundTruthContent

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
	parser.add_argument("-re", "--write-real-extension", dest='realextension', \
					help="Add a new field in the result files with the real extension", action="store_true")
	
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
		if args.realextension:
			groundtruth = args.groundtruth
		allScores = processFiles(args.filesdir)
		writeResult(allScores, args.resultfile, args.showindividualscores, args.realextension, groundtruth)
		calculateGlobalScore(args.filesdir, allScores, args.groundtruth)

if __name__ == "__main__":
   main()
