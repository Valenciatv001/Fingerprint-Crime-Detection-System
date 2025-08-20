import cv2
import numpy as np

class FingerprintPreprocessor:
    def __init__(self):
        pass
    
    def load_image(self, image_path):
        """Load fingerprint image"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        return image
    
    def convert_to_grayscale(self, image):
        """Convert image to grayscale"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def apply_histogram_equalization(self, image):
        """Apply histogram equalization for contrast enhancement"""
        return cv2.equalizeHist(image)
    
    def apply_gaussian_blur(self, image, kernel_size=(5, 5), sigma=1.5):
        """Apply Gaussian blur for noise reduction"""
        return cv2.GaussianBlur(image, kernel_size, sigma)
    
    def binarize_image(self, image, threshold=127):
        """Binarize the image using thresholding"""
        _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        return binary
    
    def preprocess(self, image_path):
        """Complete preprocessing pipeline"""
        image = self.load_image(image_path)
        gray = self.convert_to_grayscale(image)
        equalized = self.apply_histogram_equalization(gray)
        blurred = self.apply_gaussian_blur(equalized)
        binary = self.binarize_image(blurred)
        
        return {
            'original': image,
            'grayscale': gray,
            'equalized': equalized,
            'blurred': blurred,
            'binary': binary
        }