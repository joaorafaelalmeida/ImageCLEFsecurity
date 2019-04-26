import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import argparse
 

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
