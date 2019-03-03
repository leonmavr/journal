import cv2
import numpy as np
import random
import sys
from my_k_plots import *


def nearest_centroid_index(vec, centroids):
    # for my own debugging purposes
    assert vec.shape == centroids[0].shape, \
    "centroids and data vector must have the same"
    "dimensions"
    min_dis = 2**32 - 1
    for j, c in enumerate(centroids):
        if np.linalg.norm(vec - c) < min_dis:
            min_dis = np.linalg.norm(vec - c)
            j_min = j
    return j_min

def k_means(x, k, colors, conv_thr = 0.05):
    # objective function values
    J_old = 0.
    J_new = 999*conv_thr
    # randomly initialise centroids
    centroids = [random.choice(x) for _ in range(k)]
    centroids = np.array(centroids)
    while abs(J_new - J_old) > conv_thr:
        # re-assign points to clusters
        S = [[] for i in range(k)]
        J_old = J_new
        for xx in x:
            j_min = nearest_centroid_index(xx, centroids) 
            S[j_min].append(xx)
        # re-evaluate centroids
        for j in range(k):
            if len(S[j]):
                centroids[j] = [sum(S[j])[0] / len(S[j]), 
                    sum(S[j])[1] / len(S[j])]
        # update cost function
        J_new = .0
        for j in range(k):
            for xx in S[j]:
                J_new += np.linalg.norm(xx - centroids[j]) ** 2
        # plot everything
        plot_all_points(S, colors)
        plot_centroids(centroids)


def main():
    """
        Instructions:
        $ python <prog_name> <number_of_points> <number_of_clusters>
    """
    # no of data points
    n = 400 if len(sys.argv) < 2 else int(sys.argv[1])
    k = 3 if len(sys.argv) < 3 else int(sys.argv[2])
    assert k <= 100, "too many groups, see get_color_vector()"
    # actual points
    x = [] 
    for i in range(n/3):
        x.append([np.random.normal(scale = 2.5), np.random.normal(scale = 2.5)])
        x.append([np.random.normal(loc = 8., scale = 3.), \
                np.random.normal(loc = 8., scale = 3.)])
        x.append([np.random.normal(loc = -8., scale = 2.), \
                np.random.normal(loc = -8., scale = 2.)])
    x = np.array(x)
    k_means(x, k = k, colors = get_color_vector()) 

if __name__ == '__main__':
    main()
