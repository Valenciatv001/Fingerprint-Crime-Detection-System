# # system_test.py
# #!/usr/bin/env python3
# """
# Complete system test for Fingerprint Crime Detection
# """

# import requests
# import os
# import cv2
# import time

# BASE_URL = "http://127.0.0.1:5000"
# SAMPLE_DATA_DIR = "sample_data"

# def test_preprocessing():
#     """Test image preprocessing"""
#     print("Testing image preprocessing...")
    
#     from app.preprocessing import FingerprintPreprocessor
#     preprocessor = FingerprintPreprocessor()
    
#     sample_image = os.path.join(SAMPLE_DATA_DIR, "fingerprint1.jpg")
#     if os.path.exists(sample_image):
#         try:
#             result = preprocessor.preprocess(sample_image)
#             print("✅ Preprocessing successful")
#             print(f"   Generated: {len(result)} processed images")
#             return True
#         except Exception as e:
#             print(f"❌ Preprocessing failed: {e}")
#             return False
#     else:
#         print("❌ Sample image not found for preprocessing test")
#         return False

# def test_feature_extraction():
#     """Test feature extraction"""
#     print("Testing feature extraction...")
    
#     from app.preprocessing import FingerprintPreprocessor
#     from app.feature_extraction import FeatureExtractor
    
#     preprocessor = FingerprintPreprocessor()
#     extractor = FeatureExtractor()
    
#     sample_image = os.path.join(SAMPLE_DATA_DIR, "fingerprint1.jpg")
#     if os.path.exists(sample_image):
#         try:
#             preprocessed = preprocessor.preprocess(sample_image)
#             template = extractor.extract_features(preprocessed)
#             print("✅ Feature extraction successful")
#             print(f"   Found {template['num_points']} minutiae points")
#             return True
#         except Exception as e:
#             print(f"❌ Feature extraction failed: {e}")
#             return False
#     else:
#         print("❌ Sample image not found for feature extraction test")
#         return False

# def test_api_endpoints():
#     """Test all API endpoints"""
#     print("Testing API endpoints...")
    
#     # Test capture endpoint
#     print("1. Testing /capture endpoint...")
#     image_path = os.path.join(SAMPLE_DATA_DIR, "fingerprint1.jpg")
#     if os.path.exists(image_path):
#         files = {'fingerprint': open(image_path, 'rb')}
#         data = {'user_id': 1}
#         response = requests.post(f"{BASE_URL}/capture", files=files, data=data)
#         print(f"   Status: {response.status_code}")
#         if response.status_code == 201:
#             print("   ✅ Capture endpoint working")
#         else:
#             print(f"   ❌ Capture endpoint failed: {response.json()}")
#     else:
#         print("   ❌ Sample image not found")
    
#     # Test match endpoint
#     print("2. Testing /match endpoint...")
#     image_path = os.path.join(SAMPLE_DATA_DIR, "fingerprint2.jpg")
#     if os.path.exists(image_path):
#         files = {'fingerprint': open(image_path, 'rb')}
#         response = requests.post(f"{BASE_URL}/match", files=files)
#         print(f"   Status: {response.status_code}")
#         if response.status_code == 200:
#             print("   ✅ Match endpoint working")
#         else:
#             print(f"   ❌ Match endpoint failed: {response.json()}")
#     else:
#         print("   ❌ Sample image not found")
    
#     # Test records endpoint
#     print("3. Testing /records endpoint...")
#     response = requests.get(f"{BASE_URL}/records/1")
#     print(f"   Status: {response.status_code}")
#     if response.status_code == 200:
#         print("   ✅ Records endpoint working")
#     else:
#         print(f"   ❌ Records endpoint failed: {response.json()}")

# def performance_test():
#     """Test system performance"""
#     print("Testing performance...")
    
#     image_path = os.path.join(SAMPLE_DATA_DIR, "fingerprint1.jpg")
#     if os.path.exists(image_path):
#         start_time = time.time()
        
#         # Test processing time
#         from app.preprocessing import FingerprintPreprocessor
#         from app.feature_extraction import FeatureExtractor
        
#         preprocessor = FingerprintPreprocessor()
#         extractor = FeatureExtractor()
        
#         preprocessed = preprocessor.preprocess(image_path)
#         template = extractor.extract_features(preprocessed)
        
#         processing_time = time.time() - start_time
#         print(f"✅ Processing time: {processing_time:.2f} seconds")
#         print(f"   Minutiae points found: {template['num_points']}")
        
#         return processing_time
#     else:
#         print("❌ Sample image not found for performance test")
#         return None

# if __name__ == "__main__":
#     print("=" * 50)
#     print("FINGERPRINT CRIME DETECTION SYSTEM TEST")
#     print("=" * 50)
    
#     # Run all tests
#     test_preprocessing()
#     print()
#     test_feature_extraction()
#     print()
#     test_api_endpoints()
#     print()
#     performance_test()
    
#     print("\n" + "=" * 50)
#     print("SYSTEM TEST COMPLETE")
#     print("=" * 50)




# system_test.py
#!/usr/bin/env python3
"""
Complete system test for Fingerprint Crime Detection
"""

import requests
import os
import cv2
import time

BASE_URL = "http://127.0.0.1:5000"
SAMPLE_DATA_DIR = "sample_data"

def test_preprocessing():
    """Test image preprocessing"""
    print("Testing image preprocessing...")
    
    from app.preprocessing import FingerprintPreprocessor
    preprocessor = FingerprintPreprocessor()
    
    # Check if sample_data directory exists
    if not os.path.exists(SAMPLE_DATA_DIR):
        print("❌ sample_data directory not found")
        return False
    
    # Check for any image files in sample_data
    image_files = [f for f in os.listdir(SAMPLE_DATA_DIR) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    if not image_files:
        print("❌ No image files found in sample_data directory")
        return False
    
    sample_image = os.path.join(SAMPLE_DATA_DIR, image_files[0])
    
    try:
        result = preprocessor.preprocess(sample_image)
        print("✅ Preprocessing successful")
        print(f"   Processed image: {sample_image}")
        print(f"   Generated: {len(result)} processed images")
        return True
    except Exception as e:
        print(f"❌ Preprocessing failed: {e}")
        return False

def test_feature_extraction():
    """Test feature extraction"""
    print("Testing feature extraction...")
    
    from app.preprocessing import FingerprintPreprocessor
    from app.feature_extraction import FeatureExtractor
    
    preprocessor = FingerprintPreprocessor()
    extractor = FeatureExtractor()
    
    # Check if sample_data directory exists
    if not os.path.exists(SAMPLE_DATA_DIR):
        print("❌ sample_data directory not found")
        return False
    
    # Check for any image files in sample_data
    image_files = [f for f in os.listdir(SAMPLE_DATA_DIR) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    if not image_files:
        print("❌ No image files found in sample_data directory")
        return False
    
    sample_image = os.path.join(SAMPLE_DATA_DIR, image_files[0])
    
    try:
        preprocessed = preprocessor.preprocess(sample_image)
        template = extractor.extract_features(preprocessed)
        print("✅ Feature extraction successful")
        print(f"   Processed image: {sample_image}")
        print(f"   Found {template['num_points']} minutiae points")
        return True
    except Exception as e:
        print(f"❌ Feature extraction failed: {e}")
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    print("Testing API endpoints...")
    
    # Check if sample_data directory exists and has images
    if not os.path.exists(SAMPLE_DATA_DIR):
        print("❌ sample_data directory not found")
        return
    
    image_files = [f for f in os.listdir(SAMPLE_DATA_DIR) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    if not image_files:
        print("❌ No image files found in sample_data directory")
        return
    
    # Test capture endpoint
    print("1. Testing /capture endpoint...")
    image_path = os.path.join(SAMPLE_DATA_DIR, image_files[0])
    try:
        files = {'fingerprint': open(image_path, 'rb')}
        data = {'user_id': 1}
        response = requests.post(f"{BASE_URL}/capture", files=files, data=data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Capture endpoint working")
        else:
            print(f"   ❌ Capture endpoint failed: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test match endpoint
    print("2. Testing /match endpoint...")
    if len(image_files) > 1:
        image_path = os.path.join(SAMPLE_DATA_DIR, image_files[1])
    else:
        image_path = os.path.join(SAMPLE_DATA_DIR, image_files[0])
    
    try:
        files = {'fingerprint': open(image_path, 'rb')}
        response = requests.post(f"{BASE_URL}/match", files=files)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Match endpoint working")
        else:
            print(f"   ❌ Match endpoint failed: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test records endpoint
    print("3. Testing /records endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/records/1")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Records endpoint working")
        else:
            print(f"   ❌ Records endpoint failed: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def performance_test():
    """Test system performance"""
    print("Testing performance...")
    
    # Check if sample_data directory exists
    if not os.path.exists(SAMPLE_DATA_DIR):
        print("❌ sample_data directory not found")
        return None
    
    image_files = [f for f in os.listdir(SAMPLE_DATA_DIR) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    if not image_files:
        print("❌ No image files found in sample_data directory")
        return None
    
    image_path = os.path.join(SAMPLE_DATA_DIR, image_files[0])
    
    try:
        start_time = time.time()
        
        # Test processing time
        from app.preprocessing import FingerprintPreprocessor
        from app.feature_extraction import FeatureExtractor
        
        preprocessor = FingerprintPreprocessor()
        extractor = FeatureExtractor()
        
        preprocessed = preprocessor.preprocess(image_path)
        template = extractor.extract_features(preprocessed)
        
        processing_time = time.time() - start_time
        print(f"✅ Processing time: {processing_time:.2f} seconds")
        print(f"   Image: {image_files[0]}")
        print(f"   Minutiae points found: {template['num_points']}")
        
        return processing_time
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("FINGERPRINT CRIME DETECTION SYSTEM TEST")
    print("=" * 50)
    
    # Check if sample data exists
    if not os.path.exists(SAMPLE_DATA_DIR):
        print("❌ sample_data directory not found")
        print("Run: python create_sample_images.py")
    else:
        image_files = [f for f in os.listdir(SAMPLE_DATA_DIR) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
        if not image_files:
            print("❌ No image files found in sample_data")
            print("Run: python create_sample_images.py")
        else:
            print(f"Found {len(image_files)} sample images")
    
    print()
    
    # Run all tests
    test_preprocessing()
    print()
    test_feature_extraction()
    print()
    test_api_endpoints()
    print()
    performance_test()
    
    print("\n" + "=" * 50)
    print("SYSTEM TEST COMPLETE")
    print("=" * 50)