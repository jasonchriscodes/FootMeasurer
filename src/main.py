from measure import FootSizeAnalyzer
import cv2

analyzer = FootSizeAnalyzer(
    (0,0,200),
    (30,200,255)
)

# Load image
image = cv2.imread("assets/images/paper1.jpg")

image_result, foot_height, foot_width = analyzer.get_foot_size(image)

cv2.imshow("Image", image_result)
cv2.waitKey(0)
cv2.destroyAllWindows()