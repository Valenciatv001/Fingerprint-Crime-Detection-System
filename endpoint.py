
import requests
import os

BASE_URL = "http://127.0.0.1:5000"

def test_capture():
    """Test fingerprint capture endpoint"""
    print("Testing /capture endpoint...")
    
    # Use one of your sample images
    image_path = "sample_data/fingerprint1.jpg"
    
    if not os.path.exists(image_path):
        print(f"Sample image not found: {image_path}")
        return
    
    files = {'fingerprint': open(image_path, 'rb')}
    data = {'user_id': 1}
    
    try:
        response = requests.post(f"{BASE_URL}/capture", files=files, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_match():
    """Test fingerprint matching endpoint"""
    print("\nTesting /match endpoint...")
    
    # Use a different sample image for matching
    image_path = "sample_data/fingerprint2.jpg"
    
    if not os.path.exists(image_path):
        print(f"Sample image not found: {image_path}")
        return
    
    files = {'fingerprint': open(image_path, 'rb')}
    
    try:
        response = requests.post(f"{BASE_URL}/match", files=files)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_records():
    """Test records endpoint"""
    print("\nTesting /records endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/records/1")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_capture()
    test_match()
    test_records()