import cv2
import numpy as np

# download the xml from repo is search it in your installation
faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

im = cv2.imread('screenshot.png')
grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

face_rects = faceCascade.detectMultiScale(
        grey,
        scaleFactor = 1.1,
        minNeighbors = 1)
import pdb; pdb.set_trace()

for (x,y,w,h) in face_rects:
     cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.imshow("detected", im)
cv2.waitKey(0)
cv2.destroyAllWindows()
