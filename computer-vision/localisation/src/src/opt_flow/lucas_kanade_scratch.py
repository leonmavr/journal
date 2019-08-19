#!/bin/python

import cv2, numpy as np
import sys
import os

WIN_SIZE = 11

def qimshow(im, wname = 'display', timeout = 5):
    cv2.imshow(wname, im)
    cv2.waitKey(int(timeout * 1000))
    cv2.destroyAllWindows()

def grad_x(grey):
    grey = np.float32(grey)
    K = np.array([1, 0, -1])
    return cv2.filter2D(grey,
            -1,
            K,
            borderType = cv2.BORDER_REPLICATE)

def grad_y(grey):
    grey = np.float32(grey)
    K = np.array([1, 0, -1])
    return cv2.filter2D(grey.transpose(),
            -1,
            K,
            borderType = cv2.BORDER_REPLICATE).transpose()

def grad_t(grey_prev, grey_curr):
    return grey_curr - grey_prev

def gaussian(grey, mean = 0, std = 2.):
    if std > .0:
        return cv2.GaussianBlur(
                grey,
                (mean, mean),
                sigmaX = std,
                sigmaY = std) 
    else:
        return grey


def lucas_kanade(grey_prev, grey_curr, T = 5500):
    """
    Ix denotes partial derivative of matrix I w.r.t. x,
    It w.r.t time etc. Ix_Iy denotes matrix product Ix*Iy
    """
    Ix = grad_x(grey_curr)
    Iy = grad_y(grey_curr)
    It = grey_curr - grey_prev
    Ix_Ix = Ix * Ix
    Iy_Iy = Iy * Iy
    Ix_Iy = Ix * Iy
    Ix_It = Ix * It
    Iy_It = Iy * It

    Ix_Ix = gaussian(Ix_Ix)
    Iy_Iy = gaussian(Iy_Iy)
    Ix_Iy = gaussian(Ix_Iy)

    ATA = np.array(
        [[sum(sum(Ix_Ix)), sum(sum(Ix_Iy))],
        [sum(sum(Ix_Iy)), sum(sum(Iy_Iy))]]
        )
    # need eigenvalue ratio to check for corners
    lambda_1, lambda_2 = np.linalg.eig(ATA)[0][1], \
                        np.linalg.eig(ATA)[0][0]
    #x = (A^T * A)^(-1) * A^T * b
    A = []
    b = []
    rows, cols = grey_curr.shape
    for r in range(rows):
        for c in range(cols):
            A.append([Ix[r, c], Iy[r, c]])
            b.append(-It[r, c])
    A = np.float32(A)
    b = np.float32(b)

    # make sure invertible and not an edge (then l1/l2 huge)
    if np.linalg.matrix_rank(ATA) == 2 and\
    lambda_1 / lambda_2 < 10**3 and\
    lambda_1 > T and lambda_2 > T: 
        return np.dot(
                np.dot(
                    np.linalg.inv(ATA), A.transpose()),
                b)

class Feature:
    def __init__(self, tuple_xy, tuple_vec_xy):
        self._origin = tuple_xy
        self._vec = tuple_vec_xy 


def overlay(list_feat, im_prev, im_curr, debug = True):
    im = im_curr.copy()
    # opencv uses x, y notation for coordinates
    for f in list_feat:
        cv2.line(im, f._origin, (int(np.round(f._origin[0]+f._vec[0])),
            int(np.round(f._origin[1] + f._vec[1]))), (0,255,0), 2)
        cv2.circle(im,
                (int(np.round(f._origin[0] + f._vec[0])),\
                        int(np.round(f._origin[1] + f._vec[1]))),
                radius = 3,
                color = (0, 255, 0),
                thickness = 2)
    qimshow(im, timeout = 0.1)
    if debug:
        cv2.imwrite('opt_flow_vectors.png', im)
        im_inputs = np.concatenate((im_prev, im_curr), axis=1)
        cv2.imwrite('opt_flow_inputs.png', im_inputs)
    return im


def main():
    assert 2 < len(sys.argv) < 5, "Wrong cmd parameters.\
            \nUsage: python <program> <img1> <img2> <min_eigenvalue_threshold>"
    assert os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]),\
            "Input file(s) do not exist."
    im1bgr = cv2.imread(sys.argv[1]) 
    im2bgr = cv2.imread(sys.argv[2]) 
    im1 = cv2.cvtColor(im1bgr, cv2.COLOR_BGR2GRAY)
    im2 = cv2.cvtColor(im2bgr, cv2.COLOR_BGR2GRAY)
    if len(sys.argv) > 3:
        eig_thresh = int(sys.argv[3])
    else:
        eig_thresh = 12*10**3
    rows, cols = im1.shape
    feature_pts = []
    for r in range(WIN_SIZE, rows - WIN_SIZE, WIN_SIZE):
        for c in range(WIN_SIZE, cols - WIN_SIZE, WIN_SIZE):
            roi1 = im1[r - WIN_SIZE//2: r + WIN_SIZE//2 + 1,\
                    c - WIN_SIZE//2: c + WIN_SIZE//2 + 1]
            roi2 = im2[r - WIN_SIZE//2: r + WIN_SIZE//2 + 1,\
                    c - WIN_SIZE//2: c + WIN_SIZE//2 + 1]
            vec_xy = lucas_kanade(roi1, roi2, T = eig_thresh)
            if vec_xy is not None:
                feature_pts.append(Feature((c,r), tuple(vec_xy)))
    # overlay features (as vectors) on im2
    overlay(feature_pts, im1bgr, im2bgr)

main()

