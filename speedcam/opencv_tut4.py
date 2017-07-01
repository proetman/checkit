# drawing on images.
import cv2
import numpy as np


video_file='C:/Temp/x.mp4'
img_file='c:/temp/frames/frame_48.jpg'

img= cv2.imread(img_file, cv2.IMREAD_COLOR)

px = img[55,55]   # This will be the color of that pixel

print(px)   # returns this: [114 117 162]

img[55,55] = [255,255,255]

px = img[55,55]   # This will be the color of that pixel

print(px)   # returns this: [255 255 255]


# ROI = Region of Image

# Set this roi to white
#         x1:x2, y1:y2
roi = img[100:150, 400:450] = [255,255,255]
# print(roi)


# Copy and paste an ROI

wheel = img[320:420, 600:700 ]
#  100 x 100

img[0:100, 0:100] = wheel



cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
