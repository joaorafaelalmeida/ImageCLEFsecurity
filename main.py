import os
import argparse
import pathlib
import binascii
import logging as lg

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
	print(binascii.hexlify(content))

def main():
	pathlib.Path('logs').mkdir(parents=True, exist_ok=True)
	er_logger = setup_logger('error_log', 'logs/error.log')
	er_logger.info("Start")

	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--convert", help="Convert files to original format", action="store_true")
	parser.add_argument("-fh", "--file-to-hexa",  dest='filetohexa', type=str, default="",\
					help="Read and print file in hexadecimal format")
	args = parser.parse_args()

	if args.convert:
		print ("Convert files to original format")
		convertFiles(".","goldStandard")

	if args.filetohexa != "":
		readFileInHEX(args.filetohexa)


if __name__ == "__main__":
   main()