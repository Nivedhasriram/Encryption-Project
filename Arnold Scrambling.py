import matplotlib.pyplot as plt
import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import zipfile
import os


def input_dicom_image(dicom_path):
    """
    Load the DICOM image from the specified path.
    """
    try:
        dicom_image = pydicom.dcmread(dicom_path)
        return dicom_image
    except FileNotFoundError:
        print("DICOM file not found")
        return None
    except Exception as e:
        print("Error loading DICOM file:", e)
        return None

dicom_path = "Image2.dcm"
dicom_image = input_dicom_image(dicom_path)
dicom_data = pydicom.dcmread(dicom_path)
img = apply_voi_lut(dicom_data.pixel_array, dicom_data)
print(dicom_data)

def arnold_cat_map(image, iterations):
    height, width = image.shape
    print("Image shape:", image.shape)
    
    # Define the Arnold's cat map transformation matrices
    transformationMatrixHeight = np.array([[2, 1], [1, 1]])
    transformationMatrixWidth = np.array([[1, 1], [1, 2 * (width // height)]])
    
    # Apply Arnold's cat map separately to each dimension
    for i in range(iterations):
        # Apply transformation to height
        new_image_height = np.empty_like(image)
        for x in range(height):
            for y in range(width):
                old_pos = np.array([x, y])
                new_pos = np.dot(transformationMatrixHeight, old_pos) % np.array([height, width])
                new_image_height[x, y] = image[new_pos[0], new_pos[1]]
        
        # Apply transformation to width
        new_image_width = np.empty_like(image)
        for x in range(height):
            for y in range(width):
                old_pos = np.array([x, y])
                new_pos = np.dot(transformationMatrixWidth, old_pos) % np.array([height, width])
                new_image_width[x, y] = new_image_height[new_pos[0], new_pos[1]]
        
        image = new_image_width.copy()
        
    return image

ACMimg = arnold_cat_map(img.copy(), 10)

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

