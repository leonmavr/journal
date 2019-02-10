# adapted from https://stackoverflow.com/a/14617359
import sys
import cv2
import numpy as np
from scipy.ndimage import label
from matplotlib import pyplot as plt

def myimshow(im, win_name = 'display', wait_for_key = False):
    try:
        cv2.imshow(win_name, im)
        if wait_for_key:
            cv2.waitKey()
        else:
            cv2.waitKey(4000)
        cv2.destroyAllWindows()
    except Exception as e:
        print "%s\n...continuing..." % e

def plot_hist(grey):
    hist = cv2.calcHist([grey], [0], None, [256], [0,256])
    plt.plot(hist, 'g')
    plt.xlim([0, 256])
    plt.show()


def scale_from_to(arr2D, from_ = 0, to = 255):
    return (from_ * np.ones(np.array(arr2D, np.uint8).shape) + \
            ((arr2D - arr2D.min()) / (arr2D.max() - arr2D.min()) * to)).\
            astype(np.uint8)

def segment_on_dt(im, imBW):
    # generate a loose border of objects for ext markers
    border = cv2.dilate(imBW, None, iterations=5)
    border = border - cv2.erode(border, None)

    dt = cv2.distanceTransform(imBW,
            distanceType = cv2.DIST_L2,
            maskSize = 3)
    dt = scale_from_to(dt, 0, 255)
    # threshold slightly higher than half
    thr_val, dt = cv2.threshold(dt, 140, 255, cv2.THRESH_BINARY)
    # simply assigns a different integer to each conn. component
    lbl, ncc = label(dt)
    lbl = lbl * (255 / (ncc + 1))
    # Completing the markers now. 
    myimshow(np.uint8(lbl), 'lbl')
    lbl[border == 255] = 255
    myimshow(np.uint8(lbl), 'lbl')

    lbl = lbl.astype(np.int32)
    myimshow(lbl)
    cv2.watershed(im, lbl)
    # don't want the background negative
    lbl[lbl == -1] = 0
    lbl = lbl.astype(np.uint8)
    return 255 - lbl

def main():
    img = cv2.imread('img/pills.jpg')
    #myimshow(cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:,:,2])

    # Pre-processing.
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
    strel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(17,17))
    myimshow(img_gray)
    _, img_bin = cv2.threshold(img_gray, 0, 255,
            cv2.THRESH_OTSU)
    myimshow(img_bin)

    result = segment_on_dt(img, img_bin)
    myimshow(result)

    # Markers on origin BGR image
    result[result != 255] = 0
    result = cv2.dilate(result, None)
    img[result == 255] = (0, 0, 255)
    myimshow(img)

main()
