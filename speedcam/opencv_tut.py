
import cv2
import numpy as np
import matplotlib.pyplot as plt

img_file='c:/temp/frames/frame_48.jpg'

# Other options for reading, IMREAD_COLOR, IMREAD_UNCHANGED
img= cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)

# Show image in cv2
#cv2.imshow('window-name', img)
#cv2.waitKey(0)                    # wait for any key
#cv2.destroyAllWindows()

#cv2.imwrite('mynewfile.png', img)       # save to file

# show image in matplotlib

plt.imshow(img, cmap='gray', interpolation='bicubic')
plt.plot([50,100], [80,100], 'c', linewidth=5)    # c = cyan
plt.show()

