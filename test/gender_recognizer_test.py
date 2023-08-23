import sys
sys.path.insert(0,"/home/pi/ENSE810/Project/src")

import unittest
from gender_recognizer import GenderRecognizer 
from error import EmptyImageError

class GenderRecognizerTest(unittest.TestCase):
    def testEmptyImage(self):
        face1 = "assets/models/opencv_face_detector.pbtxt"
        face2 = "assets/models/opencv_face_detector_uint8.pb"
        gen1 = "assets/models/gender_deploy.prototxt"
        gen2 = "assets/models/gender_net.caffemodel"

        recognizer = GenderRecognizer(
            face1 = face1,
            face2 = face2,
            gender1 = gen1,
            gender2 = gen2
        )
        with self.assertRaises(EmptyImageError):
            recognizer.predict(None)


if __name__ == "__main__":
    unittest.main()