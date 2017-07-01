# drawing on images.
import cv2
import numpy as np


video_file='C:/Temp/x.mp4'

comp_file = 'c:/temp/opencv-template-matching-python-tutorial.jpg'
port_file = 'c:/temp/opencv-template-for-matching.jpg'

img1_file='c:/temp/frames/frame_48.jpg'
img2_file='c:/temp/frames/frame_52.jpg'


img_bgr = cv2.imread(comp_file)
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

mytemplate = cv2.imread(port_file, 0)
# print(template.shape[::-1])
# h, w, c = mytemplate.shape[::-1]   # height, width, channel
h, w = mytemplate.shape[::-1]   # height, width, channel

cv2.imshow('gray', img_gray)
res = cv2.matchTemplate(img_gray, mytemplate, cv2.TM_CCOEFF_NORMED)

threshold = 0.9
loc = np.where(res >= threshold)

for pt in zip(*loc[::-1]):
    cv2.rectangle(img_bgr, pt, (pt[0]+w, pt[1]+h), (0,255,255), 2)

cv2.imshow('dectected', img_bgr)
#
#
cv2.waitKey(0)
cv2.destroyAllWindows()
#
