import cv2
import numpy as np
import sys

g_clicks_xy = []

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
    cv2.namedWindow('input')
    cv2.setMouseCallback('input', on_click)
    while True:
        cv2.imshow('input', im)
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
            color = (0,255,0))
    qimshow(rect, wname = 'selection', delay = 3)
    return hsvt


def backproject(hsv, hsvt, rad = 9):
    # Calculating object histogram
    # In OpenCV, hue lies within [0,179]!
    hsvt_hist = cv2.calcHist([hsvt],# image
            [0, 1],                 # channel selection
            None,                   # mask
            [90, 128],              # no of bins
            [0, 180, 0, 256]        # channel ranges
            )
    # normalize histogram to [0,255] and apply backprojection
    # to get R  (ratio histogram) matrix -> R between 0 and 1
    cv2.normalize(hsvt_hist, hsvt_hist, 0, 255, cv2.NORM_MINMAX)
    R = cv2.calcBackProject([hsv],  # image
            [0,1],                  # channel selection
            hsvt_hist,              # histogram array
            [0,180,0,256],          # channel ranges
            scale = 1)
    # convolve with circular disc
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (rad, rad))
    cv2.filter2D(R, -1, disc,R)
    # Otsu's threshold
    _, R_thresh = cv2.threshold(R, 0, 255,  cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Make it 3D to AND it with the search image
    R_thresh = cv2.merge((R_thresh, R_thresh, R_thresh))
    return R_thresh 


def usage():
    str_usage = 'Run with $ python <program_name> <input_image>\n'\
    'When your input image shows up, click 2 times to define\n'\
    'a bounding box around  a sample of your object of interest.\n'\
    'Then press "q" to finish the selection.'
    print str_usage
    sys.exit(0)


def main():
    assert len(sys.argv) > 1,\
        "Run the program with -h or --help to print usage"
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        usage()
    else:
        im = cv2.imread(sys.argv[1])
    cv2.namedWindow('select area then press q')
    cv2.setMouseCallback('select area then press q', on_click)
    while True:
        cv2.imshow('select area then press q', im)
        k = cv2.waitKey()
        if k == ord('q'):
            break
    cv2.destroyAllWindows()
    hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    click_br, click_tl = g_clicks_xy[0], g_clicks_xy[1]
    w = click_br[0] - click_tl[0]
    h = click_br[1] - click_tl[1]
    rbgt = im[click_tl[1]: click_tl[1] + h, 
            click_tl[0]: click_tl[0] + w]
    hsvt = cv2.cvtColor(rbgt, cv2.COLOR_BGR2HSV)
    R_thresh  = backproject(hsv, hsvt)
    res = cv2.bitwise_and(im, R_thresh)
    qimshow(res)


if __name__ == '__main__':
    main()
