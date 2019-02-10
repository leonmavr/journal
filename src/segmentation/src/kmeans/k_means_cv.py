import numpy as np
import cv2
from matplotlib import pyplot as plt

"""
@X: input data
@k: number of clusters
"""
def kmeans_wrapper(X, k, image_as_input = False):
    if not image_as_input:
        X = np.float32(X)
    else:
        orig_shape = X.shape
        # flatten the image into a vector of BGR entries
        # so an n x 3 -> this is why -1 as first argument
        X = X.reshape((-1, 3))
    # data must be float32
    X = np.float32(X)
    type_ = cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER
    max_iter = 10
    epsilon = 1.0
    criteria = (type_, max_iter, epsilon)
    # labels returns the index of the cluster they belong in
    compactness, labels, centers = cv2.kmeans(data = X,
        K = k,
        bestLabels = None,
        criteria = criteria,
        attempts = 10,
        flags = cv2.KMEANS_RANDOM_CENTERS)
    if not image_as_input:
        # the final clusters - Kmeans output
        S = []
        for l in labels:
            S.append(X[labels.ravel() == l])
        return S, centers
    else:
        # convert data back to image
        centers = np.uint8(centers)
        # same as for l in flat labels: res.append(center[l])
        res = centers[labels.flatten()]
        res2 = res.reshape((orig_shape))
        return res2, centers


def main():
    x1 = np.random.randint(25,54,(25,4))
    x2 = np.random.randint(45,75,(25,4))
    # concatenate them in one (50,4) array
    X = np.vstack((x1, x2))
    S, centers = kmeans_wrapper(X, 2)
    # with an image
    im = cv2.imread('../kmeans/santorini.jpg') 
    cv2.imshow('input', im)
    cv2.waitKey()
    cv2.destroyAllWindows()
    assert im is not None, "Invalid input image"
    quant, centers = kmeans_wrapper(im, 8, True)
    cv2.imshow('output', quant)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
