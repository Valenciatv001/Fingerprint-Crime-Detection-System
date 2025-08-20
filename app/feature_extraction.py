import cv2
import numpy as np
from skimage.feature import peak_local_max
from skimage.morphology import skeletonize

class FeatureExtractor:
    def __init__(self):
        pass
    
    def skeletonize_image(self, binary_image):
        """Convert binary image to skeleton for minutiae extraction"""
        skeleton = skeletonize(binary_image // 255)
        return (skeleton * 255).astype(np.uint8)
    
    def extract_minutiae(self, skeleton):
        """Extract ridge endings and bifurcations"""
        # Kernel for convolution
        kernel = np.ones((3, 3), np.uint8)
        
        # Find minutiae points
        minutiae_points = []
        
        # Ridge endings (points with exactly one neighbor)
        # Bifurcations (points with exactly three neighbors)
        
        # Simplified approach using crossing number
        for i in range(1, skeleton.shape[0] - 1):
            for j in range(1, skeleton.shape[1] - 1):
                if skeleton[i, j] == 255:  # Ridge point
                    # 3x3 neighborhood
                    neighborhood = skeleton[i-1:i+2, j-1:j+2]
                    crossings = np.sum(neighborhood) // 255
                    
                    if crossings == 2:  # Ridge ending
                        minutiae_points.append((j, i, 'ending'))
                    elif crossings == 4:  # Bifurcation
                        minutiae_points.append((j, i, 'bifurcation'))
        
        return minutiae_points
    
    def create_template(self, minutiae_points):
        """Create fingerprint template from minutiae points"""
        template = {
            'num_points': len(minutiae_points),
            'endings': [point for point in minutiae_points if point[2] == 'ending'],
            'bifurcations': [point for point in minutiae_points if point[2] == 'bifurcation'],
            'all_points': minutiae_points
        }
        return template
    
    def extract_features(self, preprocessed_data):
        """Complete feature extraction pipeline"""
        binary = preprocessed_data['binary']
        skeleton = self.skeletonize_image(binary)
        minutiae = self.extract_minutiae(skeleton)
        template = self.create_template(minutiae)
        
        return template