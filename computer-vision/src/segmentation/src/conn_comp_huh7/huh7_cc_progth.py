import sys
import cv2
import numpy as np
from scipy.ndimage import label, measurements
from matplotlib import pyplot as plt
from python_algorithms.basic.union_find import UF
from scan_union import scan_union


def qimshow(im, wait = 4, wname = 'quick show'):
    cv2.namedWindow(wname)
    cv2.moveWindow(wname, 20, 20)
    cv2.imshow(wname, im)
    cv2.waitKey(wait * 1000)
    cv2.destroyAllWindows()

def scale_from_to(arr2D, from_ = 0, to = 255):
    arr2D = np.array(arr2D)
    if arr2D.min() != arr2D.max():
        return (from_ * np.ones(np.array(arr2D, np.uint8).shape) + \
                ((arr2D - arr2D.min()) / (arr2D.max() - arr2D.min()) * to)).\
                astype(np.uint8)
    else:
        return arr2D

def prog_tophat(im, min_size, max_size, step = 3): 
    """
        For all intensities i on the input image:
        Select all pixels with intensity i, call them Ii.
        Perform top hat transform on Ii with a disk element
        of size min_size to max_size and get the result Ri.
        Sum all Ri together.
    """
    rad = int((max_size - min_size) / 4)
    _, im_BW = cv2.threshold(im, 0, 255,\
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_sum = np.zeros(im_BW.shape)
    for r in range(min_size, max_size, step):
        se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r,r))
        r_large = (max_size - min_size) / 4
        se2 = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE,
                (r_large, r_large)
                )
        im_bw = cv2.morphologyEx(im_BW, cv2.MORPH_OPEN, se2)
        im_bw = cv2.erode(im_bw, se2, 2)
        im_bw = cv2.morphologyEx(im_bw, cv2.MORPH_TOPHAT, se)
        im_bw = cv2.morphologyEx(im_bw, cv2.MORPH_OPEN, se2)
        im_bw = cv2.erode(im_bw, se2, 2)
        im_sum += im_bw
    im_sum = scale_from_to(im_sum)
    return im_sum

def get_fg_values(im):
    """
        get all non-zero possible intensities of a greyscale image
    """
    return list(set(im.flatten()))[1:]

def get_centroids_bw(bw, use_scikit = True):
    """
        get centroids of a binary image as list of tuples
    """
    centroids = []
    for i in get_fg_values(bw):
        bw_i = np.zeros(bw.shape, np.uint8)
        # make pixels with value i white
        bw_i[bw == i] = 255
        if use_scikit:
            lbl, _ = label(bw_i)
        else:
            lbl = scan_union(bw_i)
        centroids.append(measurements.center_of_mass(
            bw_i, lbl, range(1,256))
            )
    centroids = sum(centroids, []) # flatten it
    centroids = [c for c in centroids if ~np.isnan(c[0])]
    return centroids


def main():
    '''
        To use the data, extract the .zip file in the img directory
        Usage:
        $ python <prog_name> <input_image> <version_to_use>
        Where:
        If version_to_use = manual, use manual one with the H-K
        algorithm,
        else use the scikit's labelling

        Manual's drawback is 4-neighbours
    '''
    assert len(sys.argv) == 3, 'wrong cmd args, usage:\n'\
    'python <prog_name> <input_image> <version>,\n'\
    'version = scikit or manual'
    img = cv2.imread(sys.argv[1])
    use_scikit = True if sys.argv[2] != 'manual' else False 
    im = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:,:,2]
    im_sum = prog_tophat(
            im, 
            min_size = 12,
            max_size = 58,
            step = 3)
    centroids = get_centroids_bw(im_sum, use_scikit)
    ### WARNING: very ugly code ###
    for c in centroids:
        cc = map(int, c)
        cc = tuple([cc[1], cc[0]])
        img = cv2.circle(img, cc , 3, (0,255,0), thickness = 2)
    ### end of ugly code ###
    qimshow(img, wait = 20)
    cv2.imwrite('out.jpg',img)


main()
