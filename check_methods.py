# check_methods.py
from app.matching import FingerprintMatcher

# Check what methods are available
matcher = FingerprintMatcher()
methods = [method for method in dir(matcher) if not method.startswith('_')]
print("Available methods in FingerprintMatcher:")
for method in methods:
    print(f"  - {method}")