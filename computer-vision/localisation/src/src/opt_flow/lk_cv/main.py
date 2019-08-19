import numpy as np
import cv2
import sys
from LkTracker import *
from MouseRoi import *


def main():
    cap = cv2.VideoCapture(sys.argv[1])
    ret, old_frame = cap.read()
    frame1 = old_frame 

    cropper = MouseRoi(frame1)
    cropper.crop()
    cropper.qimshow(cropper.get_cropped())
    (c1,r1), (c0,r0) = cropper.clicks_xy 
    
    mask_roi = np.zeros(cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY).shape, np.uint8) 
    mask_roi[:,:] = 0
    mask_roi[r0:r1,c0:c1]=255

    tracker = LkTracker()
    tracker.frame1 = frame1
    tracker.mask = mask_roi
    while True:
        ret, frame2 = cap.read()
        tracker.frame2 = frame2 
        tracker.frame2 = frame2
        tracker.calc_opt_flow()
        tracker.frame1 = frame2.copy()
        outp = tracker.draw_tracked_points(frame2)
        cv2.imshow("tracked",outp)
        cv2.waitKey(40)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
