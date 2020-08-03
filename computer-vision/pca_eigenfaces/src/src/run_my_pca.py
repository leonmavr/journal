#!/usr/bin/env python
from my_pca import pca_wrapper
import pandas as pd
import sys
import sklearn.datasets

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise SystemError("usage:\n\n."\
            "./<this_script> data_csv_file "\
            "number_of_pca_components 0|1\n, where 1 "\
            "shows the 2D plot and 0 doesn\'t")
    else:
        fname = sys.argv[1]
        n_comp = int(sys.argv[2])
        do_plot = int(sys.argv[3])
        with open(fname) as f:
            first_line = f.readlines()[0]
            try:
                [float(f) for f in first_line.split(',')]
                header = None
            except:
                header = 0

    X = pd.read_csv(fname, header = header)
    loads, scores, sign_ratios, feats =\
            pca_wrapper(X, n_comp = n_comp, do_plot = do_plot)
    if header is not None:
        with open(fname) as f:
            header = f.readlines()[0]
            feat_names = [first_line.split(',')[f] for f in feats] 
        print('The most important attributes are:\n%s' %
                ','.join(feat_names))
    else:
        feats = [str(f) for f in feats]
        print('The most important attribute indexes are:\n%s' %
                ','.join(feats))
