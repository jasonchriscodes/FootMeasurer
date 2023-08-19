# Import dependencies
from measure import FootSizeMeasurer
import cv2

# Initialization
measurer = FootSizeMeasurer(
    (0, 0, 200), 
    (30, 200, 255)
)

# Load image
image = cv2.imread("assets/images/paper1.jpg")

# Measure foot size
image_result, foot_height, foot_width = measurer.get_foot_size(image)

# Show result image 
cv2.imshow("Result", image_result)
cv2.waitKey(0)
cv2.destroyAllWindows()