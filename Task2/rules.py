import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import argparse
 
def preProcessing(file) :
    size = len(file)
    score = 0

    #weight of each rule
    rules_weight = {}
    rules_weight['sequence_1'] = 0.33
    rules_weight['sequence_2'] = 0.33
    rules_weight['sequence_3'] = 0.34

    #sequence 1
    expected_last_bytes = b'3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a'
    last_bytes = file[0 : 1260]
    if last_bytes.find(expected_last_bytes) > -1  :
        score = score + 1 * rules_weight['sequence_1']

    #sequence 2
    expected_last_bytes = b'35363738393a434445464748494a535455565758595a636465666768696a737475767778797a'
    last_bytes = file[0 : 1260]
    if last_bytes.find(expected_last_bytes) > -1  :
        score = score + 1 * rules_weight['sequence_2']

    #sequence 3
    expected_last_bytes = b'f2f3f4f5f6f7f8f9fa'
    last_bytes = file[0 : 1500]
    if last_bytes.find(expected_last_bytes) > -1  :
        score = score + 1 * rules_weight['sequence_3']
    
    return score

def hasMessage(image_path, thresh):

    #first layer
    im = cv.imread(image_path)[:,:,0]

    #lines and rows
    count = 0
    width, height = im.shape[:2]
    x = 0
    y = 0
    while(x < width - 8):
        y = 0

        while(y < height - 8):
            
            mean, std = cv.meanStdDev(im[x:x+8, y:y+8])
            if std[0][0] > 3 and std[0][0] < 4 \
                and im[x+3, y+3] == im[x+3, y+4] \
                and im[x+4, y+3] == im[x+4, y+4] \
                and im[x+3, y+3] == im[x+4, y+4] \
                and im[x+3, y+3] > im[x+5, y+5] \
                and im[x+3, y+3] > im[x+2, y+2] \
                and im[x+2, y+3] == im[x+5, y+3] \
                and im[x+1, y+3] == im[x+6, y+3] \
                and im[x+0, y+3] == im[x+7, y+3] \
                and im[x+3, y+2] == im[x+3, y+5] \
                and im[x+3, y+1] == im[x+3, y+6] \
                and im[x+3, y+0] == im[x+3, y+7] :

                count += 1
            y = y + 1
        x = x + 1

    return count > thresh
