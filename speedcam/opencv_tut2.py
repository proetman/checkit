
import cv2
import numpy as np


video_file='C:/Temp/x.mp4'


cap = cv2.VideoCapture(video_file)

fourcc = cv2.VideoWriter_fourcc (*'XVID') # ('M', 'J', 'P', 'G')      #
# out = cv2.VideoWriter('output22.avi', fourcc, 20.0, (700,1200))
out = cv2.VideoWriter('output23.avi', fourcc, 25, (640, 480))

cnt = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cnt += 1

    out.write(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', frame)    # Normal frame
    cv2.imshow('gray', gray)    # Normal frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
out.release()

