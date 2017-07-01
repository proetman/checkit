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

    laplacian = cv2.Laplacian(frame, cv2.CV_64F)
    sobelx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=5)

    edges = cv2.Canny(frame, 100, 200)   # 200 for big edges only, 50 for every edge


    cv2.imshow('orig', frame)
    cv2.imshow('laplacian', laplacian)
    cv2.imshow('edges', edges)
    cv2.imshow('sobely', sobely)



    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
# cv2.imshow('weighted', weighted)


cv2.destroyAllWindows()
cap.release()
