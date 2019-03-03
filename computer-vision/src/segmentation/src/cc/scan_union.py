import cv2
import numpy as np
from python_algorithms.basic.union_find import UF

def scan_union(im):
    uf = UF(750) # make it large enough
    lbl = np.zeros(im.shape, np.uint16) # can get high values
    largest_lbl = 0
    ###     1st scan - assign labels and build hierarchies for 
    #       neighbouring labels
    for r in xrange(im.shape[0]):
        for c in xrange(im.shape[1]):
            if im[r, c]:
                p_above = 0 if r - 1 < 0 else im[r - 1, c]
                p_left = 0 if c - 1 < 0 else im[r, c - 1]
                if p_left == p_above == 0:
                    largest_lbl += 1
                    lbl[r, c] = largest_lbl
                elif p_left and p_above == 0:
                    lbl[r, c] = lbl[r, c - 1]
                elif p_left == 0 and p_above:
                    lbl[r, c] = lbl[r - 1, c]
                else:
                    l_min, l_max =\
                        min(lbl[r, c-1], lbl[r-1, c]), \
                        max(lbl[r, c-1], lbl[r-1, c])
                    uf.union(l_min, l_max)
                    lbl[r, c] = min(lbl[r, c - 1], lbl[r-1, c])
    ### 2nd scan - re-assign child, grandchild labels to same parent
    # aka "path compression"
    for r in xrange(im.shape[0]):
        for c in xrange(im.shape[1]):
            if lbl[r, c]:
                lbl[r, c] = uf.find(lbl[r, c])
    return lbl
