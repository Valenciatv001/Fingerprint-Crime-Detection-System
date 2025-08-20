
import cv2
import numpy as np
import os

def create_sample_fingerprint(image_path, pattern_type):
    """Create a sample fingerprint-like image for testing"""
    # Create a blank image
    img = np.ones((300, 300), dtype=np.uint8) * 255
    
    if pattern_type == "whorl":
        # Create whorl pattern
        for i in range(150):
            cv2.circle(img, (150, 150), i, 0, 1)
    elif pattern_type == "loop":
        # Create loop pattern
        for i in range(100):
            cv2.ellipse(img, (150, 150), (100, 50), 0, 0, 360, 0, 1)
    elif pattern_type == "arch":
        # Create arch pattern
        for i in range(100):
            cv2.ellipse(img, (150, 200), (100, 50), 0, 180, 360, 0, 1)
    
    # Add some noise to make it look more realistic
    noise = np.random.normal(0, 25, img.shape).astype(np.uint8)
    img = cv2.add(img, noise)
    
    # Apply blur to simulate fingerprint texture
    img = cv2.GaussianBlur(img, (5, 5), 0)
    
    # Save the image
    cv2.imwrite(image_path, img)
    print(f"Created sample image: {image_path}")

# Create sample images
os.makedirs("sample_data", exist_ok=True)

sample_images = [
    ("sample_data/fingerprint1.jpg", "whorl"),
    ("sample_data/fingerprint2.jpg", "loop"),
    ("sample_data/fingerprint3.jpg", "arch"),
    ("sample_data/fingerprint4.jpg", "whorl"),
    ("sample_data/fingerprint5.jpg", "loop")
]

for image_path, pattern_type in sample_images:
    create_sample_fingerprint(image_path, pattern_type)

print("Sample fingerprint images created successfully!")