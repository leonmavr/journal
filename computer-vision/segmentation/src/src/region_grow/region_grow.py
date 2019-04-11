import sys
import numpy as np
import time
import cv2
#np.set_printoptions(threshold=np.inf)

def grow(im, segm, thr, seed = (0,0), label = 1):
	Q = [(0,0)] * im.size
	ind = 0
	Q[ind] = seed
	if label == 1:
		segm = np.zeros(im.shape, np.uint32)
		segm[seed[0], seed[1]] = label
	while ind >= 0:
                # emulates dequeue operation
		curr = Q[ind]
		ind -= 1
		x, y = curr[0], curr[1]
		segm[x,y] = label
                neighs = \
                        [(x-1,y), (x,y+1), (x+1,y), (x,y-1)]
                # use * operator to unpack tuple in arg list
                for n in neighs:
                    if in_image_area(im, *n):
                        if segm[n] == 0 and thresh(im,(x,y),n, thr):
                            segm[n] = label
                            ind += 1
                            Q[ind] = n
        return segm


def thresh(im, tuple1, tuple2, T):
	return abs(int(im[tuple1[0],tuple1[1]]) - int(im[tuple2[0],tuple2[1]])) < T 

def in_image_area(im, row, col):
    return 0 <= row < im.shape[0] and 0 <= col < im.shape[1]

def label_all_pixels(im, thr):
	label = 1
	segm = np.zeros(im.shape, np.uint8)
	segm = grow(im, segm, thr, (0,0), label)
	while len(np.where(segm == 0)[0]):
		label += 1
		row_not_lab, col_not_lab = index_not_labelled = np.where(segm == 0)
		segm = grow(im,segm,thr,(row_not_lab[0],col_not_lab[0]), label)
	return segm


def replace_with_mean(im, segm):
	label_min = np.min(segm)
	label_max = np.max(segm)
	for l in range(label_min,label_max+1):
		ind = np.where(segm == l)
		im[ind] = np.round(np.mean(im[ind])) # mean
        return im

	
def main():
        """
        Instructions:
        $ python <prog_name> </path/to/input/image> <threshold>
        """
        im = cv2.imread(sys.argv[1]) if len(sys.argv) > 1\
                else cv2.imread('sample_07_small.jpg')
        thr = int(sys.argv[2]) if len(sys.argv) > 2\
                else 30
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        lab = label_all_pixels(im_gray, thr) 
        segm = replace_with_mean(im_gray, lab)
        cv2.imshow('segmented',segm)
        cv2.waitKey()
        cv2.destroyAllWindows()
        cv2.imwrite('output.jpg', segm)

main()

