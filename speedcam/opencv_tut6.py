# drawing on images.
import cv2
import numpy as np


video_file='C:/Temp/x.mp4'
book = 'c:/temp/bookpage.jpg'
img1_file='c:/temp/frames/frame_48.jpg'
img2_file='c:/temp/frames/frame_52.jpg'


img= cv2.imread(book)



greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

retval, threshold = cv2.threshold(greyscale, 12, 255, cv2.THRESH_BINARY)

gaus = cv2.adaptiveThreshold(greyscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
retval2, otsu = cv2.adaptiveThreshold(greyscale,125, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU)


cv2.imshow('orig', img)
cv2.imshow('gray', greyscale)
cv2.imshow('gaus', gaus)
cv2.imshow('otsu', otsu)
cv2.imshow('threshold', threshold)

# cv2.imshow('weighted', weighted)

cv2.waitKey(0)
cv2.destroyAllWindows()
