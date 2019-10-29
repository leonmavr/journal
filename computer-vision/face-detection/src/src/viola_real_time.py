import cv2
import sys
import os


def test_cascade(xml, vid_file = 0):
    assert os.path.isfile(xml), "Invalid filepath to %s" %xml
    obCascade = cv2.CascadeClassifier(xml)
    video_capture = cv2.VideoCapture(vid_file)

    while True:
        _, bgr = video_capture.read()
        im = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        # minSize: minimum size for which it was trained
        objects = obCascade.detectMultiScale(
            im,
            scaleFactor = 1.1,
            minNeighbors = 3,
            minSize = (44, 44)
        )
        # Draw a rectangle around the objects 
        for (x, y, w, h) in objects:
            cv2.rectangle(bgr, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.namedWindow('det', cv2.WINDOW_NORMAL)
        cv2.imshow('det', bgr)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def main():
    xml = 'hand_44x44_19_stages_lbp.xml' if len(sys.argv) == 1\
            else sys.argv[1]
    test_cascade(xml)


if __name__ == '__main__':
    main()
