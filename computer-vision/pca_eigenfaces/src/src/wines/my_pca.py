from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
from matplotlib import pyplot as plt


##
# @brief Computers the PCA score, loadings, and eigenvalues
#
# @param X an n by D matrix, where n is the number of measurements
# @param n_compo how many of the most important scores to keep 
# @param do_plot flag to plot the 2 first PCA scores in 2D
#
# @return scores, loadings, significance_ratios,
#         most_important_feature_indices
def pca_wrapper(X, n_comp = 2, do_plot = True): 
    """
    A wrapper around sklearn's PCA. 
    The notation follows the convention in my notes!
    """
    ### pre-processing
    # centre the data 
    n = X.shape[0]
    C = np.eye(n) - 1/n*np.ones((n,1))
    X = C.dot(X)
    # whitening - variance to 1
    whiten = StandardScaler()
    X = whiten.fit_transform(X)
    ### execute PCA
    model = PCA(n_components = n_comp).fit(X)
    loads = model.components_
    scores = model.transform(X)
    sign_ratios = model.explained_variance_ratio_
    ### Post-processing and plotting
    # For each loading we keep, find its entry (feature)
    # with the highest abs value. That's the most important
    # feature of each loading. d is the #components
    d = model.components_.shape[0]
    ind_most_important = [np.abs(model.components_[i]).argmax()\
            for i in range(d)]
    if do_plot:
        plt.title('2D visualisation')
        plt.scatter(scores[:,0], scores[:,1], marker = 'x')
        plt.xlabel('PC0')
        plt.ylabel('PC1')
        plt.grid()
        plt.show()
    return scores, loads, sign_ratios, ind_most_important
