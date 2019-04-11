import sys
import cv2
import numpy as np
from scipy.ndimage import label
from matplotlib import pyplot as plt
from skimage.morphology import reconstruction

def myimshow(im, wname = 'display', timeout = 4):
    cv2.imshow(wname, im)
    cv2.waitKey(timeout * 1000)
    cv2.destroyAllWindows()
    
im = cv2.imread('pears.png')
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_eq = cv2.equalizeHist(im)
se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
se_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (18, 18))
im_dil = cv2.dilate(im_eq, se)
myimshow(im_dil)
im_op = cv2.morphologyEx(im_dil, cv2.MORPH_OPEN, se)
im_cl = cv2.morphologyEx(im_dil, cv2.MORPH_CLOSE, se)
im_bw = cv2.adaptiveThreshold(im_cl, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
        cv2.THRESH_BINARY, 95, 0) 
im_bw = cv2.erode(im_bw, se, iterations = 2)
im_bw = cv2.morphologyEx(im_bw, cv2.MORPH_OPEN, se_large)
myimshow(im_bw, timeout = 100)
