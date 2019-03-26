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


def main():
    im = cv2.imread(sys.argv[1]) # input image
    cv2.namedWindow('select area')
    cv2.setMouseCallback('select area', on_click)
    while True:
        cv2.imshow('select area', im)
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
    qimshow(rbgt)
    hsvt = cv2.cvtColor(rbgt, cv2.COLOR_BGR2HSV)
    # Calculating object histogram
    # In OpenCV, hue lies within [0,179]!
    hsvt_hist = cv2.calcHist([hsvt],    # image\
            [0, 1],                         # channel selection\
            None,                           # mask\
            [90, 128],                      # no of bins\
            [0, 180, 0, 256]                # channel ranges\
            )
    # normalize histogram to [0,255] range and apply backprojection
    cv2.normalize(hsvt_hist, hsvt_hist, 0, 255, cv2.NORM_MINMAX)
    dst = cv2.calcBackProject([hsv],  # image\
            [0,1],                          # channel selection\
            hsvt_hist,                        # histogram array\
            [0,180,0,256],                  # channel ranges\
            scale = 1)
    # Now convolute with circular disc
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    cv2.filter2D(dst, -1, disc,dst)
    # Otsu's threshold
    _, thresh = cv2.threshold(dst, 0, 255,  cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Make it 3D to AND it with the model image
    thresh = cv2.merge((thresh, thresh, thresh))
    res = cv2.bitwise_and(im,thresh)

    cv2.imshow('Original', im)
    cv2.imshow('Result', res)
    cv2.waitKey()
    cv2.destroyAllWindows()
    # res = np.vstack((model, thresh,res))
    # cv2.imwrite('res.jpg',res)

if __name__ == '__main__':
    main()
