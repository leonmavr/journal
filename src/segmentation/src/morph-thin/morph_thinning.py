import cv2, numpy as np
import sys

def thin(im, se):
    return im - cv2.morphologyEx(im, cv2.MORPH_HITMISS, se);

def get_golay_letters():
# golay alphabet
    B1 = np.array(([-1, -1 ,-1],
                    [0, 1, 0],
                    [1, 1, 1]), 
                    np.int8)
    B2 = np.array(([0, -1 ,-1],
                    [1, 1, -1],
                    [1, 1, 0]), 
                    np.int8)
    B3 = np.array(([1, 0 ,-1],
                    [1, 1, -1],
                    [1, 0, -1]), 
                    np.int8)
    B4 = np.array(([1, 1 ,0],
                    [1, 1, -1],
                    [0, -1, -1]), 
                    np.int8)
    B5 = np.array(([1, 1 ,1],
                    [0, 1, 0],
                    [-1, -1, -1]), 
                    np.int8)
    B6 = np.array(([0, 1 ,1],
                    [-1, 1, 1],
                    [-1, -1, 0]), 
                    np.int8)
    B7 = np.array(([-1, 0 ,1],
                    [-1, 1, 1],
                    [-1, 0, 1]), 
                    np.int8)
    B8 = np.array(([-1, -1 ,0],
                    [-1, 1, 1],
                    [0, 1, 1]), 
                    np.int8)
    return [B1,B2,B3,B4,B5,B6,B7,B8]

def thin_by_se(im, se):
    return im - cv2.morphologyEx(im, cv2.MORPH_HITMISS, se);

def thin(im):
    im_old = np.zeros(im.shape, np.uint8)
    im_new = im
    while np.sum(abs(im_old - im_new)) > 100:
        im_old = im_new
        for bi in get_golay_letters():
            im_new = thin_by_se(im_new, bi) 
    return im_new

def main():
    """
        Usage:
        $ python <image_filename>
    """
    im = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    _, im = cv2.threshold(im, 50,255,cv2.THRESH_BINARY_INV) 
    cv2.imshow('BW', im)
    cv2.waitKey()
    cv2.imshow('thinned', thin(im))
    cv2.waitKey()
    cv2.destroyAllWindows()

main()
