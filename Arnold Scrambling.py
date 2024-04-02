import matplotlib.pyplot as plt
import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import zipfile
import os

# Load the DICOM image
zip_file_path = "Image.zip"

# Name of the DICOM file within the zip folder
dicom_filename = "Image.dcm"

# Extract the DICOM file from the zip folder
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract(dicom_filename)

# Load DICOM image from the extracted folder
dicom_path = dicom_filename
dicom_data = pydicom.dcmread(dicom_path)
img = apply_voi_lut(dicom_data.pixel_array, dicom_data)

# Define the Arnold's cat map function
def arnold_cat_map(image, iterations):
    height, width = image.shape
    assert height == width, "Image should be square"
    assert height % 2 == 0, "Image size should be even"
    transformationMatrix = np.array([[2, 1], [1, 1]])

    for i in range(iterations):
        for x in range(height):
            for y in range(width):
                old_pos = np.array([x, y])
                new_pos = np.dot(transformationMatrix, old_pos) % height
                image[x, y] = image[new_pos[0], new_pos[1]]
    return image

# Apply Arnold's cat map to the DICOM image
ACMimg = arnold_cat_map(img.copy(), 10)

# Plotting
plt.figure(figsize=(12, 10))

# Original DICOM Image
plt.subplot(221)
plt.imshow(img, cmap='gray', vmin=np.min(img), vmax=np.max(img))
plt.title('Original DICOM Image')

# Arnold's Cat Map Image
plt.subplot(222)
plt.imshow(ACMimg, cmap='gray', vmin=np.min(ACMimg), vmax=np.max(ACMimg))
plt.title("Arnold's Cat Map DICOM Image")

# Original DICOM Image Histogram
plt.subplot(223)
plt.hist(img.ravel(), bins=256, range=(0, np.max(img)), color='blue', alpha=0.7)
plt.title('Original DICOM Image Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

# Arnold's Cat Map DICOM Image Histogram
plt.subplot(224)
plt.hist(ACMimg.ravel(), bins=256, range=(0, np.max(ACMimg)), color='red', alpha=0.7)
plt.title("Arnold's Cat Map DICOM Image Histogram")
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
