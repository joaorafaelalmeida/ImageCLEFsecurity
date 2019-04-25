import os
import argparse
import pathlib
import binascii
import logging as lg
from os import listdir
from os.path import isfile, join
import rules

JPG_MN = "FF D8 FF DB"
GIF_MN = "47 49 46 38 37 61"
PDF_MN = "25 50 44 46 2d"
PNG_MN = "89 50 4E 47 0D 0A 1A 0A"

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

def processFiles(dir, reultFile, groundtruth, writeScore=False):
	allFiles = [f for f in listdir(dir) if isfile(join(dir, f))]
	for file in allFiles:
		fileInProcess = readFileInHEX(dir+"/"+file)
		score = {}
		score["jpg"] = rules.isJPG(fileInProcess)
		print (score)


def main():
	pathlib.Path('logs').mkdir(parents=True, exist_ok=True)
	pathlib.Path('results').mkdir(parents=True, exist_ok=True)
	er_logger = setup_logger('error_log', 'logs/error.log')

	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--convert", help="Convert files to original format", action="store_true")
	parser.add_argument("-fh", "--file-to-hexa",  dest='filetohexa', type=str, default="",\
					help="Read and print file in hexadecimal format")
	parser.add_argument("-p", "--process", help="Process the files and compare with the ground truth", action="store_true")
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
		processFiles(args.filesdir, args.resultfile, args.groundtruth)

if __name__ == "__main__":
   main()