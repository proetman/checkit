# drawing on images.
import cv2
import numpy as np


video_file='C:/Temp/x.mp4'
book = 'c:/temp/bookpage.jpg'
img1_file='c:/temp/frames/frame_48.jpg'
img2_file='c:/temp/frames/frame_52.jpg'

cap = cv2.VideoCapture(video_file)

while True:
    _, frame = cap.read()

    # hsv = hue, sat, value (look in wiki)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_road = np.array([100,0,0])
    upper_road = np.array([125,255,255])

    mymask = cv2.inRange(hsv, lower_road, upper_road)
    # mask_inv = cv2.bitwise_not(mymask)
    res = cv2. bitwise_and(frame, frame, mask=mymask)

    # erosion
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(mymask, kernel, iterations = 1)
    dilation = cv2.dilate(mymask, kernel, iterations = 1)

    opening = cv2.morphologyEx(mymask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(mymask, cv2.MORPH_CLOSE, kernel)

    # tophat is diff betwen input image and opening of the image
    # cv2.imshow('tophad', tophad)
    # blackhat is diff between closing of input image and the image.
    # cv2.imshow('blackhat', blackhat)

    # dilation

    #    kernel = np.ones((15,15), np.float32)/225
    #    smoothed = cv2.filter2D(res, -1, kernel)
    #    blur = cv2.GaussianBlur(res, (15,15), 0)
    #    median = cv2.medianBlur(res, 15 )
    #    bilat = cv2.bilateralFilter(res, 15, 75,75)

    cv2.imshow('res', res)
    cv2.imshow('opening', opening)
    cv2.imshow('closing', closing)
    # cv2.imshow('bilat', bilat)
    # cv2.imshow('smoothed', smoothed)
    # cv2.imshow('mymask', mymask)
    # cv2.imshow('res', res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
# cv2.imshow('weighted', weighted)


cv2.destroyAllWindows()
cap.release()
