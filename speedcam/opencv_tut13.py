# drawing on images.
import cv2
import numpy as np
import matplotlib.pyplot as plt

video_file='C:/Temp/x.mp4'

img1_file='c:/temp/frames/frame_48.jpg'
img2_file='c:/temp/frames/frame_52.jpg'

img_file = 'c:/temp/opencv-corner-detection-sample.jpg'

img = cv2.imread(img_file)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)

corners = cv2.goodFeaturesToTrack(gray, 200, 0.01, 10)  # img, how many to find, quality, distance apart

corners = np.int0(corners)

for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x,y), 3, 255, -1)

cv2.imshow('corner', img)
#
cv2.waitKey(0)
cv2.destroyAllWindows()
#
