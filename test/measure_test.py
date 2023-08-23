import sys
sys.path.insert(0,"/home/pi/ENSE810/Project/src")

import unittest
from measure import Point, FootSizeMeasurer
from error import EmptyImageError

class PointTest(unittest.TestCase):
    def testGetTupleFromPoint(self):
        point = Point()
        point.x = 1
        point.y = 1
        self.assertEqual(point.tuple(), (1,1), "get tuple from point fail")
    
    def testPointConstructor(self):
        point = Point(3,4)
        self.assertEqual(point.x, 3, "coordinate x not equal ")
        self.assertEqual(point.y, 4, "coordinate y not equal ")

class FootSizeMeasurerTest(unittest.TestCase):
    def testEmptyImage(self):
        measurer = FootSizeMeasurer(
            paper_hsv_min = (0, 0, 200), 
            paper_hsv_max = (180, 255, 255)
        )
        with self.assertRaises(EmptyImageError):
            measurer.get_foot_size(None, 1)


if __name__ == "__main__":
    unittest.main()