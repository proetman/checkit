# drawing on images.
import cv2
import numpy as np


video_file='C:/Temp/x.mp4'
img_file='c:/temp/frames/frame_48.jpg'

img= cv2.imread(img_file, cv2.IMREAD_COLOR)


#   image, start line loc, end line loc, colour, thickness
# Blue = 255,0,0, Green = 0,255,0; red = 0,0,255,
# white = 255,255,255;   black = 0,0,0
cv2.line(img, (0,0), (300,300), (255,255,255), 15)

# rectangle, top left, bot right,
cv2.rectangle(img, (10,10), (200,150), (50,50,50), 4)

# circle, centre, radius, -1 = fill
cv2.circle(img, (500,500), 100, (0,0,255), -1 )

# polygon
pts = np.array([[10,5],[20,30],[70,20], [50,10]], np.int32)
# pts = pts.reshape((-1,1,2))
# true for connect final point to first point
# colour
cv2.polylines(img, [pts], True, [0,255,255], 3 )

# writing
font = cv2.FONT_HERSHEY_SIMPLEX
# size = 0.5
cv2.putText(img, 'Open CV Tut', (600,600), font, 0.5, (200,255,255), 2, cv2.LINE_AA )

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
