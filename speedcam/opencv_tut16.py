# drawing on images.
import cv2
import numpy as np
# import matplotlib.pyplot as plt

video_file='C:/Temp/x.mp4'

img1_file='c:/temp/frames/frame_48.jpg'
img2_file='c:/temp/frames/frame_52.jpg'

cap = cv2.VideoCapture(video_file)
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)

    cv2.imshow('orig', frame)
    cv2.imshow('fg', fgmask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
#
#cv2.imshow('img1_file', img1)
#cv2.imshow('img2_file', img2)
##
# cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
#
