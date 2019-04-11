from __future__ import print_function  
import cv2
import numpy as np
import sys


g_clicks_xy = []

######### UI #########
def qimshow(im, delay = 10, wname = 'display'):
    cv2.imshow(wname,im)
    cv2.waitKey(delay * 1000)
    cv2.destroyAllWindows()


def on_click(event, x, y, flags, param):
    """
    Mouse callback function - write to global list of clicks
    """
    global g_clicks_xy
    if event == cv2.EVENT_LBUTTONDOWN:
        g_clicks_xy.append((x, y))

######### Maths #########
def is_in_circle(centre, r, point):
    return (centre[0] - point[0])**2 + (centre[1] - point[1])**2 <= r**2

def centroid(pts2D):
    x, y =zip(*pts2D)
    N = len(x)
    return int(sum(x)/N), int(sum(y)/N)

def dist(x, y):
    x, y = np.asarray(x), np.asarray(y)
    return np.linalg.norm(x - y)

######### Mean Shift process #########
def backproject(hsv, hsvt, rad = 9):
    # Calculating object histogram
    # In OpenCV, hue lies within [0,179]!
    hsvt_hist = cv2.calcHist([hsvt],# image
        [0, 1], # channel selection
        None, # mask
        [90, 128], # no of bins
        [0, 180, 0, 256] # channel ranges
        )
    # normalize histogram to [0,255] and apply backprojection
    # to get R (ratio histogram) matrix -> R between 0 and 1
    cv2.normalize(hsvt_hist, hsvt_hist, 0, 255, cv2.NORM_MINMAX)
    R = cv2.calcBackProject([hsv], # image
        [0,1], # channel selection
        hsvt_hist, # histogram array
        [0,180,0,256], # channel ranges
        scale = 1)
    # convolve with circular disc
    if rad:
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (rad, rad))
        cv2.filter2D(R, -1, disc,R)
        # Otsu's threshold
    _, R_thresh = cv2.threshold(R, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Make it 3D to AND it with the search image
    #R_thresh = cv2.merge((R_thresh, R_thresh, R_thresh))
    return R_thresh

"""
@bw: thresholded backprojected frame (M x N)
@x: current mean shift vector estimation (tuple)
@h: mean shift ROI radius (int)
@<return>: new mean shift vector estimation (tuple)
"""
def my_mean_shift(bw, x, h, conv_thresh = 2.0):
    """
    This mean shift works as follows:
    @bw is black and white image obtained as the  result of thesholding
    the backprojected frame with the model, model being a small sample
    of the object of interest extracted by the user.
    The domain is simply the xy, and for the update of m.s. vector x only
    white pixels up to h pixels around the current x are considered. White     pixels are most likely to be part of the OOI. The updated x is returned
    """
    x_old = (np.inf, np.inf)
    while dist(x_old, x) > conv_thresh:
        started = True
        x_old = x
        points_in = []
        for r in range(bw.shape[0]):
            for c in range(bw.shape[1]):
                if bw[r, c] and is_in_circle(x, h, (c, r)): 
                    points_in.append((c, r))
                    x = centroid(points_in)
    print (x)
    #qimshow(cv2.circle(bw.copy(), x, 6, 126, 4),  delay = 0)
    #qimshow(bw)
    return x


"""
@im: The input image as read (in BGR)
"""
def get_model(im):
    """
    Process user input (clicks) and Extract the target image
    (model) in hsv.
    """
    global g_clicks_xy
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    cv2.namedWindow('2 clicks, then press q')
    cv2.setMouseCallback('2 clicks, then press q', on_click)
    while True:
        cv2.imshow('2 clicks, then press q', im)
        k = cv2.waitKey()
        if k == ord('q'):
            break
    cv2.destroyAllWindows()
    # for clicks, index 0 = x, index 1 = y
    g_clicks_xy = sorted(g_clicks_xy, 
            key = lambda x: x[0]**2 + x[1]**2,
            reverse = True) [-2:]
    click_br, click_tl = g_clicks_xy[0], g_clicks_xy[1]
    w = click_br[0] - click_tl[0]
    h = click_br[1] - click_tl[1]
    hsvt = hsv[click_tl[1]: click_tl[1] + h, 
            click_tl[0]: click_tl[0] + w]
    rect = cv2.rectangle(im.copy(), g_clicks_xy[0], g_clicks_xy[1], 
            color = (0, 255, 0))
    qimshow(rect, wname = 'selection', delay = 3)
    return hsvt


def usage():
    str_usage = \
    "Instructions:\n\
    Run the program with\n\
    $ python <prog_name> <video> <roi_radius>\n\
    When the \"input\" window appears, click 2 times to create a \n\
    bounding box around a sample of the object to be tracked.\n\
    Then press \"q\" to continue.\n"
    print(usage)


######### Driver #########
def main():
    """
    Instructions:
    Run the program with
    $ python <prog_name> <video> <roi_radius>"
    When the "input" window appears, click 2 times to create a 
    bounding box around a sample of the object to be tracked.
    Then press "q" to continue.
    """
    assert len(sys.argv) > 1,\
            "\nUsage: $ python <prog_name> <video> <roi_radius>.\n\
            Run with $ python -h to print detailed instructions"
    if sys.argv[1] in ['-h', '--help']:
        usage()

    vid_path = sys.argv[1]
    h = 20 if len(sys.argv) == 2 else int(sys.argv[2])
    cap = cv2.VideoCapture('soccer2.mp4')
    _, frame1 = cap.read()
    # Get model (target) image
    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsvt = get_model(frame1)

    bw = backproject(hsv, hsvt, rad = 0)

    # Initialise mean shift (x) vector from user input
    click_br, click_tl = g_clicks_xy[0], g_clicks_xy[1]
    w = click_br[0] - click_tl[0]
    h = click_br[1] - click_tl[1]
    x = (click_tl[0] + w/2, click_tl[1] + h/2)
    valid = True
    # frame by frame processing
    while(valid):
        valid, im = cap.read()
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        bw = backproject(hsv, hsvt, rad = 0)
        x = my_mean_shift(bw, x, h) 
        cv2.imshow('detection', cv2.circle(im.copy(), x, 1, (0, 255, 0),
            6))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the capture
    cap.release()
    cv2.destroyAllWindows()


main()
