# Import dependencies
import numpy as np
import cv2
from  math import sqrt

class FootSizeAnalyzer:
    def __init__(self, paper_hsv_min: tuple, paper_hsv_max: tuple, paper_height=297, paper_width=210):
        self.__paper_hsv_min = paper_hsv_min
        self.__paper_hsv_max = paper_hsv_max
        self.__paper_height = paper_height
        self.paper_width = paper_width

    def get_foot_size(self, image):
        foot_height = 0
        foot_width = 0 

        image_result = image

        image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

        image_thresh = cv2.inRange(image_hsv, self.__paper_hsv_min, self.__paper_hsv_max)

        contours, _ = cv2.findContours(image_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for point in cnt:
            x = point[0]
            y = point[1]

            r = 
        cv2.drawContours(image_result, contours, 0, (0,255,0), 3)

        return image_result, foot_height, foot_width