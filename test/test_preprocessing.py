import unittest
import cv2
import numpy as np
from app.preprocessing import FingerprintPreprocessor

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.preprocessor = FingerprintPreprocessor()
        # Create a test fingerprint image
        self.test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        cv2.imwrite('test_fingerprint.png', self.test_image)
    
    def test_load_image(self):
        image = self.preprocessor.load_image('test_fingerprint.png')
        self.assertIsNotNone(image)
        self.assertEqual(image.shape, (100, 100, 3))
    
    def test_grayscale_conversion(self):
        image = self.preprocessor.load_image('test_fingerprint.png')
        gray = self.preprocessor.convert_to_grayscale(image)
        self.assertEqual(len(gray.shape), 2)
    
    def test_histogram_equalization(self):
        image = self.preprocessor.load_image('test_fingerprint.png')
        gray = self.preprocessor.convert_to_grayscale(image)
        equalized = self.preprocessor.apply_histogram_equalization(gray)
        self.assertEqual(equalized.shape, gray.shape)
    
    def test_gaussian_blur(self):
        image = self.preprocessor.load_image('test_fingerprint.png')
        gray = self.preprocessor.convert_to_grayscale(image)
        blurred = self.preprocessor.apply_gaussian_blur(gray)
        self.assertEqual(blurred.shape, gray.shape)
    
    def tearDown(self):
        import os
        if os.path.exists('test_fingerprint.png'):
            os.remove('test_fingerprint.png')

if __name__ == '__main__':
    unittest.main()