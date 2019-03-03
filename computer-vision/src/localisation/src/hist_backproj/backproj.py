import cv2, numpy as np
import sys
import pdb

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


"""
@hsv: The whole input (search) image in hsv
@hsvt: The target (model), i.e. the ROI, in hsv
@<return>: The ration histogram of hsvt by hsv, clipped from 0 to 1
"""
def ratio_histogam(hsv, hsvt):
    # see doc: HS histograms, [0, 180] as in OpenCV 0 <= H <= 179
    M = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    I = cv2.calcHist([hsvt], [0, 1], None, [180, 256], [0, 180, 0, 256])
    R = np.divide(np.array(M, np.float),
            np.array(I, np.float),
            out = np.zeros_like(I),
            where = I != 0)
    R[R > 1.0] = 1.0
    return R


"""
@hsv: the whole input image in HSV
@R: the ratio histogram as returned by the ratio_histogram function
@r: the radius of the disk backprojection convolves with
"""
def backproject(hsv, R, rad = 15):
    """
        Generate a 2D binary image where ones are probably the object(s)
        of interest and zeros the background
    """
    b = np.zeros((hsv.shape[0], hsv.shape[1]), np.uint8)
    for r in range(hsv.shape[0]):
        for c in range(hsv.shape[1]):
            b[r,c] = R[hsv[r,c][0], hsv[r,c][1]]
    b = np.uint8(b)
    disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (rad, rad))
    # convolve with disk
    b = cv2.filter2D(b, -1, disk, b)
    b = np.uint8(b)
    b = np.array(cv2.normalize(b, b, 0, 255, cv2.NORM_MINMAX), np.uint8)
    _, thresh = cv2.threshold(np.uint8(b), 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU )
    return thresh


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
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    hsvt = get_model(im)
    R = ratio_histogam(hsv, hsvt)    
    thresh = backproject(hsv, R)
    # final processing - AND the 2D binary threshold image with the
    # original RGB input image to show the result
    thresh = cv2.merge((thresh, thresh, thresh))
    res = cv2.bitwise_and(im, thresh)
    qimshow(res)


if __name__ == '__main__':
    main()
