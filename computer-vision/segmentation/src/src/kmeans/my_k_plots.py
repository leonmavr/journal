from matplotlib import pyplot as plt
import numpy as np
import random

def rgb2hex(r, g, b):
    return "#%02x%02x%02x".upper() % (r, g, b)

def get_color_vector():
    # N <= k (number of classes)
    N = 100 
    vec = [(0,0,0) for _ in range(N)]
    for nn in range(N):
        r, b, g = \
                random.randint(0, 255), random.randint(0,255),\
                random.randint(0, 255)
        vec[nn] = rgb2hex(r, g, b)
    return vec

"""
@S: the set of (k) clusters of data points
@color_vec: a vector of RGB colours in hex #RRGGBB
"""
def plot_all_points(S, color_vec):
    for Si, cv in zip(S, color_vec):
        x = map(lambda x: x[0], Si)
        y = map(lambda x: x[1], Si)
	plt.scatter(x, y, color = cv )

"""
@centroids: the set of (k) centroid vectors
"""
def plot_centroids(centroids):
    cx = map(lambda x: x[0], centroids)
    cy = map(lambda x: x[1], centroids)
    plt.scatter(cx, cy, color = '#000000' )
    plt.show()
