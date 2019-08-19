import numpy as np
import cv2


class MouseRoi:
    """
    # Sample usage:
    cropper = MouseRoi(im)
    cropper.crop()
    # then:
    cropper.qimshow(cropper.get_cropped())
    # or:
    (c1,r1), (c0,r0) = cropper.clicks_xy
    """
    def __init__(self, im):
        if im is not None:
            assert type(im) is np.ndarray, \
                "Wrong input. Fundamental type must be np.nparray."
        self._im = im
        self.clicks_xy = []
        cv2.namedWindow('input')
        cv2.setMouseCallback('input', self.on_click)
     
    def on_click(self, event, x, y, params, flag):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicks_xy.append((x, y))

    def get_cropped(self, show_whole_image = False):
        assert len(self.clicks_xy) != 0,\
            "You have not selected the area to crop.\n\
            Click on the top left and bottom right of the object."
        # get last two (x, y) clicks
        self.clicks_xy = sorted(self.clicks_xy, 
            key = lambda x: x[0]**2 + x[1]**2,
            reverse = True) [-2:]
        click_br, click_tl = self.clicks_xy[0],\
            self.clicks_xy[1]
        w = click_br[0] - click_tl[0]
        h = click_br[1] - click_tl[1]
        cv2.destroyAllWindows()
        if show_whole_image:
            ret = cv2.rectangle(self._im.copy(),
                    self.clicks_xy[0],
                    self.clicks_xy[1], 
                    color = (60,255,0),
                    thickness = 2)
            return ret 
        else:
            x, y = click_tl[0], click_tl[1]
            ret = self._im[y:y + h, x:x + w]
            return ret

    def crop(self):
        while True:
            cv2.imshow('input', self._im)
            k = cv2.waitKey()
            if k == ord('q'):
                break

    @staticmethod
    def qimshow(im, wname = 'display', timeout = 5):
        cv2.imshow(wname, im)
        cv2.waitKey(timeout * 1000)
        cv2.destroyAllWindows()
