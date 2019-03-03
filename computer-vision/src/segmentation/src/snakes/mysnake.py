import numpy as np
import cv2
from itertools import * 
from math import *
import sys
import pdb

g_pts = []

##############################################
#    Mouse callbacks
##############################################
def on_click(event,x,y,flags,param):
    global pts
    if event == cv2.EVENT_LBUTTONDOWN:
        #print x,y
        g_pts.append((x,y))
def get_gradient_img(im,\
        mask = np.array([[1,0,-1],\
            [2,0,-2],
            [1,0,-1]])):
    # to detect horizontal edges
    mask = mask.transpose()
    _ = im.copy().copy()
    im = cv2.GaussianBlur(im, (15,15), 1.8, _,  1.8)
    return cv2.filter2D(im, -1, mask)


##############################################
#   Algo calculations 
##############################################
"""
@iterable:
@size: window width
@<return>: a list that contains tuples
credits: https://stackoverflow.com/a/6822907
"""
def window(iterable, size = 2):
    iters = tee(iterable, size)
    for i in xrange(1, size):
        for each in iters[i:]:
            next(each, None)
    return list(izip(*iters))

def avg_dist(points):
    distances = [norm(np.array(p1) - np.array(p2)) for p1, p2 in combinations(points, 2)]
    avg_distance = sum(distances) / len(distances)
    return avg_distance

"""
L-2 norm
"""
def norm(vec):
    return np.linalg.norm(vec)

"""
Total curve energy E = E_elastic + E_bending + E_external,
as defined in active contour model. E depends on a, b, c coeff/s.
"""
def total_energy(points, im_grad, a, b, c):
    points = map(np.array, points)
    energy = 0.
    plen = len(points)
    for i, p in enumerate(points):
        row, col = points[i]
        M = np.max(im_grad[row-1:row+2, col-1:col+2])
        m = np.min(im_grad[row-1:row+2, col-1:col+2])
        if m != M:
            eExt = - c * norm((im_grad[row,col] - m) / (M - m))
        else:
            eExt = 0.
        eElas = a * (norm(points[(i+1)%plen] - points[i%plen]) - avg_dist(points))**2 
        eBend = b * norm(points[(i-1)%plen] - 2 * points[i] + points[(i+1)%plen])**2 
        energy += eElas + eBend + eExt 
    return energy

"""
Greedy snakes energy minimisation.
Runs through each point the curve, moving the point in all posible 
position at a 5x5 window around it location. Finds energy at each move.
When energy is min, the point is locked to that position and scans next point.
"""
def min_energy_coords(im, im_grad, points, a, b, c):
    r_min, c_min = -1, -1
    energy = 0.
    for i, p in enumerate(points):
        eMin = 2**32 - 1 
        r, c = points[i]
        for rr in range(r-3, r+4):
            for cc in range(c-3, c+4):
                points[i] = np.array([rr,cc])
                energy = total_energy(points, im_grad, a, b, c)
                if energy < eMin:
                    eMin = energy
                    r_min, c_min = rr, cc
        points[i] = np.array([r_min, c_min])
        energy = .0
    return points

##############################################
#  Main 
##############################################
def main():
    """
    Usage:
        $ <program_name> <input_image> <iterations> <alpha> <beta> <gamma>
    When the program is run, it will show a grey image of the input.
    Select some points around the object you want to segment by clicking
    on them. When done, press <Enter>.
    Note:  the stopping condition is simply the number of iter/s.
    """
    im_name = 'mito.jpg' if len(sys.argv) < 2 else sys.argv[1]
    nIters = 30 if len(sys.argv) < 3 else int(sys.argv[2])
    a = 1.2 if len(sys.argv) < 4 else float(sys.argv[3])
    b = 1. if len(sys.argv) < 5 else float(sys.argv[4])
    c = 0.45 if len(sys.argv) < 6 else float(sys.argv[5])
    
    imBGR = cv2.imread(im_name)
    im = cv2.cvtColor(imBGR, cv2.COLOR_BGR2GRAY)
    im_grad = get_gradient_img(im)
    cv2.namedWindow('image')	
    cv2.setMouseCallback('image', on_click)
    cv2.imshow('image', im)
    cv2.waitKey() 
    cv2.destroyAllWindows()
    points = g_pts
    for i in range(nIters):
        points = min_energy_coords(im, im_grad, points, a , b, c)
        imcircle = imBGR.copy().copy()
        for p in points: # p tutple
            cv2.circle(imcircle, (p[0], p[1]), 5, (0,0,255), -1)
        cv2.imshow('im',imcircle)
        cv2.waitKey(100)
    #g_pts
    #TODO: draw a line between each pair of points
    points.append(points[0])
    for p1, p2 in zip(points, points[1:]):
        cv2.line(imcircle, tuple(p1), tuple(p2), (0,0,255))
    cv2.imshow('im',imcircle)
    cv2.waitKey(4000)
    cv2.destroyAllWindows()

main()
