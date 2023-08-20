import numpy as np
import cv2

image = np.zeros((480, 320, 3))

image[:,100:,:] = image[:,100:,:] + (255,255,0)

image2 = image[:,100:,:]

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.GR

