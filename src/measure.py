# Import dependencies
import numpy as np
import cv2
from math import sqrt

class Point:
    '''
        A class which holds coordinate of pixel in an image
    '''
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def tuple(self):
        '''
            Get tuple representation
        '''
        return (self.x, self.y)

class FootSizeMeasurer:
    '''
        Class for measure foot size on top of white paper
    '''

    def __init__(
        self, paper_hsv_min: tuple, 
        paper_hsv_max: tuple, 
        paper_height = 297, paper_width = 210, # Default paper size 29.7 x 21 cm 
        pixel_per_mm = 5,
    ):
        # Initialize class member
        self.__paper_hsv_min = paper_hsv_min
        self.__paper_hsv_max = paper_hsv_max
        self.__paper_height = paper_height
        self.__paper_width = paper_width

        self.__pixel_per_mm = pixel_per_mm

    def __get_corner(self, cnt, h, w):
        '''
            Return 4 corner points of a contour.
            
            Param:
            [cnt] contour to be analyzed
            [h] image height
            [w] image width

            Distance between 4 image corner and all points in the contour are calculated.
            Then, points with minimum distance between each image corner
            are recognized as the 4 corner    
        '''

        # Minimum distance of points in the contour
        # Use big number for initialization
        r_min_tl = 1000000
        r_min_tr = 1000000
        r_min_bl = 1000000
        r_min_br = 1000000

        # Result of 4 corner
        point_tl = Point()
        point_tr = Point()
        point_bl = Point()
        point_br = Point()

        # Check all points in the contour
        for point in cnt:
            x = point[0][0] # x coordinate of the pixel
            y = point[0][1] # y coordinate of the pixel

            # Calculate distance between point and each image corner
            r_tl = sqrt(x**2 + y**2)
            r_tr = sqrt((w-x)**2 + (y)**2)
            r_bl = sqrt((x)**2 + (h-y)**2)
            r_br = sqrt((w-x)**2 + (h-y)**2)

            # Minimize distance
            
            if r_tl < r_min_tl: # Top-left corner
                r_min_tl = r_tl
                point_tl.x = x
                point_tl.y = y

            if r_tr < r_min_tr: # Top-right corner
                r_min_tr = r_tr
                point_tr.x = x
                point_tr.y = y

            if r_bl < r_min_bl: # Bottom-left corner
                r_min_bl = r_bl
                point_bl.x = x
                point_bl.y = y

            if r_br < r_min_br: # Bottom-right corner
                r_min_br = r_br
                point_br.x = x
                point_br.y = y

        return point_tl, point_tr, point_bl, point_br
    
    def __determine_foot_size(self, image):
        '''
            Return foot size in mm

            Param: 
            [image] binary image which contains object of foot
        '''
        # Define foot width and foot height
        w_foot = 0
        h_foot = 0

        # Extract image height and width
        h, w = image.shape

        # Find contours of the binary image
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours from largest to smallest contour area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Get contour with largest contour area
        cnt = contours[0]

        y_min = 100000
        x_min = 100000
        x_max = 0

        # Margin of the foot object in the image (in mm)
        margin_left = 40 * self.__pixel_per_mm 
        margin_right = 40 * self.__pixel_per_mm 
        margin_top = 20 * self.__pixel_per_mm 
        margin_bottom = 100 * self.__pixel_per_mm 

        # Helper point to get outer point of the foot object
        point_left = Point()
        point_right = Point()
        point_top = Point()
        
        # Check all points in the contour
        for point in cnt:
            x = point[0][0] # x coordinate of the pixel
            y = point[0][1] # y coordinate of the pixel

            # Ignore points in the margin
            if x < margin_left or x > (w - margin_right): continue
            if y < margin_top or y > (h - margin_bottom): continue

            # Minimize top point
            if y < y_min:
                y_min = y
                point_top.x = x
                point_top.y = y

            # Minimize left point
            if x < x_min:
                x_min = x
                point_left.x = x
                point_left.y = y

            # Minimize right point
            if x > x_max: 
                x_max = x
                point_right.x = x
                point_right.y = y

        # Calculate foot size
        w_foot = (x_max - x_min) / self.__pixel_per_mm
        h_foot = (h - y_min) / self.__pixel_per_mm

        return (w_foot, h_foot), (point_left, point_right, point_top)

    def get_foot_size(self, image):
        '''
            Return foot size from raw image

            Param:
            [image] RGB image which contains foot object on top of white paper
        '''

        # Initialize foot height and foot width
        foot_height = 0
        foot_width = 0

        # Copy raw image
        image_result = image

        # Extract image height and image width
        h, w, _ = image.shape

        # Convert raw image colorspace to HSV
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Convert HSV image to binary image
        image_thresh = cv2.inRange(image_hsv, self.__paper_hsv_min, self.__paper_hsv_max)
        
        # Find contours of the binary image
        contours, _ = cv2.findContours(image_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours from largest to smallest contour area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Get contour with largest contour area
        cnt = contours[0]

        # Get 4 corner points of the paper object
        point_tl, point_tr, point_bl, point_br = self.__get_corner(
            cnt=cnt,
            h=h, w=w
        )

        ''' 
            Transform the paper object into flat image 
        '''

        # Size of the transformed image
        w_transformed = self.__paper_width * self.__pixel_per_mm 
        h_transformed = self.__paper_height * self.__pixel_per_mm 

        # Reference points of the paper object
        input_pts = np.float32(
            [
                point_tl.tuple(),
                point_tr.tuple(),
                point_bl.tuple(),
                point_br.tuple()
            ]
        )

        # Transformed points
        output_pts = np.float32(
            [
                (0, 0),
                (w_transformed, 0),
                (0, h_transformed),
                (w_transformed, h_transformed)
            ]
        )

        # Get transformation matrix 
        M = cv2.getPerspectiveTransform(input_pts,output_pts)

        # Warp binary image to be used for analyzing foot size 
        image_warped = cv2.warpPerspective(image_thresh,M,(w_transformed, h_transformed),flags=cv2.INTER_LINEAR)

        # Warp original image to be used for displaying the result
        image_result = cv2.warpPerspective(image_result,M,(w_transformed, h_transformed),flags=cv2.INTER_LINEAR)

        # Determine foot size and reference points of foot object
        foot_size, foot_coordinate = self.__determine_foot_size(image_warped)

        # Extract foot size and foot coordinate
        foot_width, foot_height = foot_size
        point_left, point_right, point_top = foot_coordinate
   
        # Append result as text
        image_result = cv2.putText(image_result, 
                                   f'Height: {foot_height} mm', 
                                   (50, 50), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, (255, 0, 0), 2, cv2.LINE_AA)
        image_result = cv2.putText(image_result, 
                                    f'Width: {foot_width} mm', 
                                    (50, 100), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, (255, 0, 0), 2, cv2.LINE_AA)
        
        # Mark foot object
        image_result = cv2.line(image_result, point_left.tuple(), (point_right.x, point_left.y), (0,0,255), 3)
        image_result = cv2.line(image_result, point_top.tuple(), (point_top.x, h), (0,0,255), 3)

        image_result = cv2.rectangle(image_result, (point_left.x, point_top.y), (point_right.x, h), (0,255,0), 3)

        return image_result, foot_height, foot_width