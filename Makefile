t1-runTestSet:
	cd Task1 && python3 main.py -pt -d ../AllDataSets/Test\ Set\ Task\ 1

t1-runTrainingSetSmall:
	cd Task1 && python3 main.py -p

t1-runTrainingSetComplete:
	cd Task1 && python3 main.py -p -d ../AllDataSets/Training\ set\ Task\ 1