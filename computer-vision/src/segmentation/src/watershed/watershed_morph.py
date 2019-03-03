import cv2
import numpy as np
from scipy.ndimage import label
from skimage.morphology import reconstruction


def myimshow(im, wname = 'display', timeout = 4):
    cv2.imshow(wname, im)
    cv2.waitKey(timeout * 1000)
    cv2.destroyAllWindows()

"""
    @im: greyscale image
    @rad: radius of structuting element
    @thr_size: adaptive threshold size
    @im_bw: BW image of white connected components 
"""
def to_BW_markers(im, rad, thr_size):
	im_eq = cv2.equalizeHist(im)
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (rad, rad))
    se_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, \
            (2 * rad, 2 * rad))
    im_dil = cv2.dilate(im_eq, se)
    im_op = cv2.morphologyEx(im_dil, cv2.MORPH_OPEN, se)
    im_cl = cv2.morphologyEx(im_dil, cv2.MORPH_CLOSE, se)
    im_bw = cv2.adaptiveThreshold(im_cl, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY, thr_size, 0) 
    im_bw = cv2.erode(im_bw, se, iterations = 2)
    im_bw = cv2.morphologyEx(im_bw, cv2.MORPH_OPEN, se_large)
    return im_bw

"""
    @imBGR
    @im_bw: bw image of connected components
    @ncc: number of cc's
    @lbl: labelled greyscale incl. object borders
"""
def get_labels(imBGR, im_bw):
    lbl, ncc = label(im_bw)
	# reslace; ncc + 1 cc's to account for border
    lbl = lbl * (255 / (ncc + 1))
    border = cv2.dilate(im_bw, None) - cv2.dilate(im_bw, None)
    lbl[border == 255] = 255
    lbl = lbl.astype(np.int32)
	# watershed(m * n * 3 np.int32, m * n)
    cv2.watershed(imBGR, lbl)
    lbl[lbl == -1] = 0
    lbl = lbl.astype(np.uint8)
    return ncc, lbl

def main():
    imBGR = cv2.imread('img/pears.png')
    im = cv2.cvtColor(imBGR, cv2.COLOR_BGR2GRAY)
    im_bw = to_BW_markers(im, 9, 105)
    ncc, lbl = get_labels(imBGR, im_bw)
    # overlay
    imBGR[lbl == 0] = (0,0,255)
    myimshow(imBGR, wname = 'final', timeout = 10)

if __name__ == '__main__':
    main()