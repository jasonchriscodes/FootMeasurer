import numpy as np
import cv2

image = cv2.imread("paper.jpg")
image = cv2.resize(image, (400,600), interpolation = cv2.INTER_AREA)
# HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
thresh1 = cv2.inRange(hsv,(11,0,180),(25,101,255))

cv2.imshow("image", image)
cv2.imshow("hsv", hsv)
cv2.imshow("thresh", thresh1)

cv2.waitKey(0)
cv2.destroyAllWindows()