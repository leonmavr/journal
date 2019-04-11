import numpy as np
import cv2
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

def main():
    cap = cv2.VideoCapture(sys.argv[1])
    # take first frame of the video
    ret,frame = cap.read()
    # setup initial location of window
    r,h,c,w = 250,90,400,125  # simply hardcoded the values
    track_window = (c,r,w,h)
    # set up the ROI for tracking
    roi = frame[r:r+h, c:c+w]
    hsv_roi = get_model(frame)
    click_br, click_tl = g_clicks_xy[0], g_clicks_xy[1]
    w = click_br[0] - click_tl[0]
    h = click_br[1] - click_tl[1]
    x = click_tl[0] 
    y = click_tl[1] 
    track_window = (x, y, w, h)
    #hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # Filter out noise
    mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)),
            np.array((180.,255.,255.)))
    roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
    cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
    # Setup the termination criteria,
    #either 10 iteration or move by atleast 1 pt
    term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
    while(1):
        ret ,frame = cap.read()
        if ret == True:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
            # apply meanshift to get the new location
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)
            # Draw it on image
            x,y,w,h = track_window
            img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
            cv2.imshow('img2',img2)
            k = cv2.waitKey(30) & 0xff
            if k == ord('q'):
                break
        else:
            break
    cv2.destroyAllWindows()
    cap.release()

main()
