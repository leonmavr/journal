import pdb
import cv2, numpy as np
from collections import namedtuple
import sys
from math import pow, ceil, log

Rectangle = namedtuple('Rectangle','rl cl rh ch')


class QNode:
    """
    Members:
        @_im: the *current* part of the input image stored in
        the node
        @_children: a list of 4 QNode for each QNode
        @_rect: a rectangle that when projected in the *input*
        image gives the current stored portion
    Methods:
        @get_width: image block width
        @get_height: image block heigh
    """
    def __init__(self, im, (rl, cl), (rh, ch)):
        assert rh >= rl and ch >= cl, \
                "the first row, column pair must be the low one"\
                "and the next the high"
        self._im = im[rl:rh, cl:ch]
        self._children = [None for _ in range(4)]
        # TODO: this not used much for now, 
        # can be used to tidy up the divide method...
        self._rect = Rectangle(rl, cl, rh, ch) 
        
    def get_width(self):
        return self._rect.ch - self._rect.cl

    def get_height(self):
        return self._rect.rh - self._rect.rl


class QTree:
    """
    Members:
        @_thr: std threshold that helps define the split condition;
        If the std of the image portion in the node is larger than that,
        then recursively split it in 4 children (see QNode)
        @_root: The QNode root of the quadtree, stores the whoe image.
        Stored image must be a power of 2
        @_segm: The output (segmented image)
        @_min_size: Minimum block size when splitting the image in 4 quadrants
        (children)
        @_orig_im_size
    Methods:
        @divide(qtree_root): recusrively divide the root in 4 quadrant depending
        on whether the splitting condition (std and block size) is met.
        At the same time, when we can't divide further, then write the mean of 
        the block to the segmented image
        @find_leaves(): return all quadtree leaves in a list
        @pad_to_po2(): pad the input image size to a square with side equal
        the next power of 2
        @show_image(): shortcut for displaying the output image
        @get_image(): returns the segmented image cropped to the original size
    """
    def __init__(self, im, thr, min_size = 1):
        assert type(im) == np.ndarray and len(im.shape) == 2,\
            "quadtree needs a grayscale image as input"
        self._thr = thr
        # will need original size to crop is after padding, see next lines
        self._orig_im_size = im.shape
        # make sure size of im is square po2 to copy with divisions by 2
        im = self.pad_to_po2(im)
        self._root = QNode(im,\
                    (0,0),\
                    tuple(im.shape))
        self._segm = np.zeros(self._root._im.shape, np.uint8)
        self._min_size = min_size
        
    def divide(self, qnode, (r0, c0) = (0,0)):
        if np.std(qnode._im) < self._thr or qnode._im.size == self._min_size:
            delta_r, delta_c = qnode.get_height(), qnode.get_width()
            self._segm[r0: r0+delta_r, c0: c0+delta_c] = \
                    np.uint8(np.mean(qnode._im)) 
            return qnode
        else:
            im = qnode._im
            rows, cols = im.shape
            self.divide(\
                QNode(im, (0,0), (rows/2, cols/2)),(r0, c0) )
            self.divide(
                QNode(im, (0,cols/2), (rows/2, cols)), (r0, c0 + cols/2) )
            self.divide(
                QNode(im, (rows/2, 0), (rows, cols/2)), (r0+rows/2, c0) )
            self.divide(
                QNode(im, (rows/2, cols/2), (rows, cols)), (r0+rows/2, c0+cols/2) )

    # TODO: fix this method
    def find_leaves(self, qnode):
        leaves = []
        if qnode._children.count(None) == 4:
            return leaves.append(qnode)
        else:
            for c in qnode._children:
                leaves.append(find_leaves(c, leaves))
        return leaves

    @staticmethod
    def pad_to_po2(arr):
        max_dim = max(arr.shape)
        nextpo2 = int( pow(2, ceil(log(max_dim)/log(2))) )
        return cv2.copyMakeBorder( src = arr,\
                top = 0,\
                bottom = nextpo2 - arr.shape[0],\
                left = 0,\
                right = nextpo2 - arr.shape[1],\
                borderType = cv2.BORDER_REFLECT_101)
        
    def show_image(self):
        cv2.imshow('QTree: segmented', 
            self._segm[:self._orig_im_size[0], :self._orig_im_size[1]])
        cv2.waitKey()
        cv2.destroyAllWindows()

    def get_segm_image(self):
        return self._segm[:self._orig_im_size[0], :self._orig_im_size[1]]

