# drawing on images.
import cv2
import numpy as np
import matplotlib.pyplot as plt

video_file='C:/Temp/x.mp4'

img1_file='c:/temp/frames/frame_48.jpg'
img2_file='c:/temp/frames/frame_52.jpg'

img1 = cv2.imread(img1_file, 1)
img2 = cv2.imread(img2_file, 1)

orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

matches = bf.match(des1, des2)
matches = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[0:80], None, flags=2)
plt.imshow(img3)
plt.show()
#
#cv2.imshow('img1_file', img1)
#cv2.imshow('img2_file', img2)
##
cv2.waitKey(0)
cv2.destroyAllWindows()
#
