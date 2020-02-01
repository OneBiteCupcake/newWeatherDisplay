import unittest
import SmDisplay


class MyTestCase(unittest.TestCase):
    def test_convertWindBearing(self):
        self.assertEquals(SmDisplay.convertWindBearing(15), "N")


if __name__ == '__main__':
    unittest.main()
