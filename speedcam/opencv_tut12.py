# drawing on images.
import cv2
import numpy as np
import matplotlib.pyplot as plt

video_file='C:/Temp/x.mp4'

img1_file='c:/temp/frames/frame_48.jpg'
img2_file='c:/temp/frames/frame_52.jpg'


img = cv2.imread(img1_file)

mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1,65), np.float64)
fgdModel = np.zeros((1,65), np.float64)

rect = (161, 79, 850, 550)  # outside this rectangle will be removed

cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
plt.imshow(img)
plt.colorbar()
plt.show()

#
cv2.waitKey(0)
cv2.destroyAllWindows()
#
