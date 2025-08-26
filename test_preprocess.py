import cv2
from matplotlib import pyplot as plt

path = r"uploads\eze.jpeg"
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

# Enhance contrast
img_eq = cv2.equalizeHist(img)

# Threshold (binarization)
_, img_thresh = cv2.threshold(img_eq, 127, 255, cv2.THRESH_BINARY)

# Show results
plt.subplot(1,3,1); plt.imshow(img, cmap='gray'); plt.title("Original")
plt.subplot(1,3,2); plt.imshow(img_eq, cmap='gray'); plt.title("Equalized")
plt.subplot(1,3,3); plt.imshow(img_thresh, cmap='gray'); plt.title("Thresholded")
plt.show()
