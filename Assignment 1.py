# -*- coding: utf-8 -*-
"""CV-Assignment 1(10.14EVEN).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lWDgOEjBHjN3D4eRmpYOLYdEugHJzx1w
"""

# Step 1: Install OpenCV and other necessary libraries, as well as the Tesseract OCR tool
!sudo apt update
!sudo apt install tesseract-ocr
!pip install opencv-python pytesseract numpy matplotlib

# Import necessary libraries
import cv2
import pytesseract
from google.colab import files# Upload files locally and associate with the next step
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

#Step 2: Upload images from local storage, allowing for more flexible image selection
uploaded = files.upload()
# Load the image
for filename in uploaded.keys():
    image_path = filename

# Read an image
image = cv2.imread(image_path)

# Step 3: Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display grayscale image
plt.imshow(gray_image, cmap='gray')
plt.title('Grayscale image ')
plt.show()

# Step 4: Apply blurring to reduce noise in the image, using Gaussian blur
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Display the blurred image
plt.imshow(blurred_image, cmap='gray')
plt.title('Fuzzy image ')
plt.show()

# Step 5: Apply binarization to enhance image contrast
# Use Otsu's binarization method to automatically determine the optimal threshold
_, binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Display the binarized image
plt.imshow(binary_image, cmap='gray')
plt.title('Binarized image ')
plt.show()

# Step 6: Detect text in the image using morphological text region detection
# Perform morphological transformation
# First closing and then opening operations to remove small noise points and connect text regions
kernel = np.ones((1, 1), np.uint8)
closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
opened_image = cv2.morphologyEx(closed_image, cv2.MORPH_OPEN, kernel)

# Find the outline
contours, _ = cv2.findContours(opened_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw bounding boxes on the original image
boxed_image = image.copy()
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(boxed_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
# Display the image after drawing the bounding box
plt.imshow(cv2.cvtColor(boxed_image, cv2.COLOR_BGR2RGB))
plt.title('image after delineating the bounding box')
plt.axis('off')
plt.show()

#Step 7: Use Tesseract tool to extract text from the detected area
if contours:
    x, y, w, h = cv2.boundingRect(contours[0])
    cropped_image = binary_image[y:y+h, x:x+w]  #Crop out the text area
    pil_image = Image.fromarray(cropped_image)  #Convert to PIL image
    text = pytesseract.image_to_string(pil_image, lang='eng')  #Extract text, specify language as English

    #Display the extracted text on the image
    cv2.putText(boxed_image, text.strip(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    #Display images with extracted text
    plt.imshow(cv2.cvtColor(boxed_image, cv2.COLOR_BGR2RGB))
    plt.title('Images with extracted text')
    plt.show()
else:
    print("No text area detected")

#Step 8: Print the extracted text
if contours:
    print("Extracted text content:")
    print(text.strip())