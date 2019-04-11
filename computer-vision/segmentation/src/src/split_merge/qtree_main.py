"""
    Split and merge segmentation based on paper by Horowitz & 
    Pavlidis.
    This is the driver for the quadtree (QTree) class, which
    implements the split part only.
"""
import cv2
from qtree import *


def main():
    """
    Usage:
        python <prog_name> </path/to/image> <std_threshold>
    """
    sys.setrecursionlimit(10000000)
    im = cv2.imread(sys.argv[1]) if len(sys.argv) > 1\
        else cv2.imread('img/ship_240x240.jpg')
    thr_std = float(sys.argv[2]) if len(sys.argv) > 2\
        else 14.
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    qtree = QTree(im, thr_std)
    qtree.divide(qtree._root)
    qtree.show_image()
    cv2.imwrite('output_thr_%.2f.png' % thr_std, \
            qtree.get_segm_image())


if __name__ == '__main__':
    main()
