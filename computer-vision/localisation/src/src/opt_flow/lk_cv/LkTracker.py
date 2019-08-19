import cv2
import numpy as np


class LkTracker:
    """
    For usage, see:
    https://gist.github.com/0xLeo/c5f9cc9e23b9a4f6f07f9149492806df
    """
    def __init__(self,
            max_conrners = 100,
            quality_level = 0.2,
            min_distance = 10,
            block_size = 3,
            win_size = (15, 15),
            max_level = 6,
            criteria = (cv2.TERM_CRITERIA_EPS\
                | cv2.TERM_CRITERIA_COUNT, 10, 0.03)):
        assert .0 <= quality_level <= 1.,\
            "corner quality level must be a float from 0 to 1"
        assert type(win_size) is tuple,\
            "win_size must be a tuple"
        # feature params - used for cv2.goodFeaturesToTrack 
        self._feature_params = dict(maxCorners = max_conrners,
                qualityLevel = quality_level,
                minDistance = min_distance,
                blockSize = block_size)
        self._lk_params = dict(
                winSize = win_size,
                maxLevel = max_level,
                criteria = criteria)
        self._mask = None
        # LK params - for cv2.calcOpticalFlowPyrLK
        self._first_time = True
        # configs - use only valid feature points from previous frame
        #self._use_old_points = True
        self._p0 = None
        self._p1 = None
    @property
    def frame1(self):
        return self._frame1
    @frame1.setter
    def frame1(self, bgr):
        assert len(bgr.shape) == 3,\
                "Wrong input. Input is a BGR image"
        self._frame1 = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    @property
    def frame2(self):
        return self._frame2
    @frame2.setter
    def frame2(self, bgr):
        assert len(bgr.shape) == 3,\
                "Wrong input. Input is a BGR image"
        self._frame2 = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    @property
    def mask(self):
        return self._mask
    @mask.setter
    def mask(self, mask):
        assert type(mask) is np.ndarray and \
                all([m == 0 or m == 255 for m in mask.ravel()]), \
                "mask must be an np.uint8 matrix of 0s and 255s"
        self._mask = mask

    def calc_opt_flow(self, mask = None):
        if self._first_time:
            self._p0 = cv2.goodFeaturesToTrack(self.frame1,
                    mask = self.mask,
                    **self._feature_params)
            self._first_time = False
            # all points valid status (st)
        else:
            p1, st, err = cv2.calcOpticalFlowPyrLK(self.frame1,
                    self.frame2,
                    self._p0,
                    mask,
                    **self._lk_params)
            # Select good points
            self._p1 = p1
            good_new = self._p1[st==1]
            good_old = self._p0[st==1]
            self._p0 = good_new.reshape(-1,1,2)


    def draw_tracked_points(self, bgr = None):
        st = np.ones((self._p0.shape[0], 1), np.uint8)
        pts = self._p0[st == 1]
        if bgr is None:
            im = self.frame2
        else:
            im = bgr
        for p in pts:
            im_drawn = cv2.circle(im, tuple(p), 3, (0, 255, 0), 2)
        return im_drawn

    @staticmethod
    def qimshow(im, wname = 'display', timeout = 5):
        cv2.imshow(wname, im)
        cv2.waitKey(timeout * 1000)
        cv2.destroyAllWindows()
