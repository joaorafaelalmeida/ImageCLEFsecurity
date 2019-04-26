import os
import argparse
import pathlib
import binascii
import logging as lg
from os import listdir
from os.path import isfile, join
import rules

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

pathlib.Path('logs').mkdir(parents=True, exist_ok=True)
pathlib.Path('results').mkdir(parents=True, exist_ok=True)
er_logger = setup_logger('error_log', 'logs/error.log')

def processFiles(dir, threshould, dstdir=None):
	allFiles = [f for f in listdir(dir) if isfile(join(dir, f))]
	allScores = {}
	for file in allFiles:
		fileInProcess = readFileInHEX(dir+"/"+file)
		score = rules.preProcessing(fileInProcess)
		if (score == 0):
			score = "0"
		else:
			score = rules.hasMessage(dir+"/"+file, threshould)
			if(score):
				score = "1"
			else:
				score = "0"

				if dstdir:
					f = open(dir+"/"+file, 'rb')
					fileInProcess = f.read()
					pathlib.Path(dstdir).mkdir(parents=True, exist_ok=True)
					with open(dstdir + "/" + file, 'wb') as out_file:
						out_file.write(fileInProcess)
						out_file.close()
		#Structure is: file:(type, {scores..})
		allScores[file] = score
		print(file + " " + score)
	return allScores

def writeResult(allScores, resultFile, writeScore=False, writeRealExtension=False, groundtruth=""):
	f = open(resultFile, "w")
	if writeRealExtension:
		groundTruthContent = readGroundTruth(groundtruth)
	for score in allScores:
		result = score.split(".")[0] + ";" + allScores[score]
		f.write(result+"\n")
	f.close()

def readGroundTruth(groundtruth):
	groundTruthContent = []
	f = open(groundtruth, "r")
	for x in f:
		groundTruthContent += [x.split("\n")[0]]
	return groundTruthContent

def showScores(dir, allScores, groundtruth):
	totalAlteredImages, totalImages, fail, scored, detectedAlteredImages, allDetectedAlteredImages = calculateScores(dir, allScores, groundtruth)

	precision=detectedAlteredImages/allDetectedAlteredImages
	recall=detectedAlteredImages/totalAlteredImages
	fMeasure=2*(precision*recall)/(precision+recall)

	print("\n\n+ + + Scores + + +\n")
	print("Total of images in directory: " + str(totalImages))
	print("Fails: " + str(fail))
	print("Scored: " + str(scored))
	print("Percentage of success: " + str((scored*100)/totalImages))
	print("Precision: " + str(precision))
	print("Recall: " + str(recall))
	print("F-Measure: " + str(fMeasure))

def calculateScores(dir, allScores, groundtruth):
	alteredImages = 0
	totalImages = 0
	fail = 0
	scored = 0
	detectedAlteredImages = 0
	allDetectedAlteredImages = 0
	groundTruthContent = readGroundTruth(groundtruth)
	
	allFiles = [f for f in listdir(dir) if isfile(join(dir, f))]
	for file in allFiles:
		matching = [s for s in groundTruthContent if file.split(".")[0] in s][0]
		realExtension = matching.split(";")[1]
		myPrevision = allScores[file]


		totalImages += 1
		if(realExtension == '1'): #Altered
			alteredImages += 1
			if(myPrevision == '1'):
				detectedAlteredImages += 1
				allDetectedAlteredImages += 1
		else:#realExtension = extension
			if(myPrevision == '0'):#Bad prevision
				allDetectedAlteredImages += 1


		if(realExtension != myPrevision):
			fail += 1
		else:
			scored += 1
	return (alteredImages, totalImages, fail, scored, detectedAlteredImages, allDetectedAlteredImages)

def readFileInHEX(filename):
	with open(filename, 'rb') as f:
		content = f.read()
	return binascii.hexlify(content)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--convert", help="Convert files to original format", action="store_true")
	parser.add_argument("-fh", "--file-to-hexa",  dest='filetohexa', type=str, default="",\
					help="Read and print file in hexadecimal format")
	
	parser.add_argument("-p", "--process", help="Process the files and compare with the ground truth", action="store_true")
	parser.add_argument("-pt", "--process-test-set", dest='processtest', \
					help="Run with the test set", action="store_true")
	
	parser.add_argument("-d", "--dir-of-files",  dest='filesdir', type=str, default="T2DataSet",\
					help="Directory with files to process (Default: T2DataSet)")	
	parser.add_argument("-rf", "--result-file",  dest='resultfile', type=str, default="results/task2.txt",\
					help="Result file with the classification of each file (Default: results/task2.txt)")
	parser.add_argument("-gt", "--ground-truth",  dest='groundtruth', type=str, \
					default="../GroundTruthDataSet/ground_truth_training_set_task_2.txt",\
					help="Ground truth text file (Default: ../GroundTruthDataSet/ground_truth_training_set_task_2.txt)")

	parser.add_argument("-dd", "--destination-dir",  dest='dstdir', type=str, default="ConvertedDataSet",\
					help="Directory to write the files in the original format (Default: ConvertedDataSet)")

	parser.add_argument("-t", "--threshould",  dest='threshould', type=int, default=5,\
					help="Threshould counter for marks on the picture (Default: 5)")

	parser.add_argument("-ss", "--show-individual-scores", dest='showindividualscores', \
					help="Add a new field with in the result file with the scores", action="store_true")
	parser.add_argument("-re", "--write-real-extension", dest='realextension', \
					help="Add a new field in the result files with the real extension", action="store_true")
	args = parser.parse_args()

	if args.process:
		print ("Process files...\n\n")
		allScores = processFiles(args.filesdir, args.threshould)
		writeResult(allScores, args.resultfile, args.showindividualscores, args.realextension, args.groundtruth)
		showScores(args.filesdir, allScores, args.groundtruth)

	if args.processtest:
		allScores = processFiles(args.filesdir, args.threshould, args.dstdir)
		writeResult(allScores, args.resultfile)

if __name__ == "__main__":
   main()
