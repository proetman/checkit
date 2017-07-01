# drawing on images.
import cv2
import numpy as np


video_file='C:/Temp/x.mp4'
img1_file='c:/temp/frames/frame_48.jpg'
img2_file='c:/temp/frames/frame_52.jpg'


img1= cv2.imread(img1_file, cv2.IMREAD_COLOR)
img2 = cv2.imread(img2_file, cv2.IMREAD_COLOR)
img2 = img2[350:700, 350:700]

# add = img1 + img2

# cv2.add will add the individual values of each pixel, truncating at 255
# (155,211,79) + (50,170,200) = 205, 381,279 ==> 205,255,255
# add = cv2.add(img1, img2)

# weighted = cv2.addWeighted(img1, 0.6, img2, 0.4, 0)

rows, cols, channels = img2.shape
roi = img1[0:rows, 0:cols]
img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#if above 220, then convert to white, otherwise convert to black; then INVERSE
ret, mask = cv2.threshold(img2gray, 100, 255, cv2.THRESH_BINARY_INV)

# cv2.imshow('mask', mask)

# This makes anything white in the original img2 to clear; then draws that on img1
# creates a mask of the image shape.

mask_inv = cv2.bitwise_not(mask)
img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
img2_fg = cv2.bitwise_and(img2, img2, mask=mask)


dst = cv2.add(img1_bg, img2_fg)
img1[0:rows, 0:cols] = dst

cv2.imshow('image', img1)
cv2.imshow('image2', img2)

# cv2.imshow('weighted', weighted)

cv2.waitKey(0)
cv2.destroyAllWindows()
