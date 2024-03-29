import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import pydicom
import os
import zipfile

@njit()
def arnold_cat_map(image):
    height, width = image.shape[:2]
    scrambled_image = np.zeros_like(image)

    for i in range(height):
        for j in range(width):
            new_i = (i + 2 * j) % height  # Modify the row index calculation
            new_j = (i + 3 * j) % width   # Modify the column index calculation
            scrambled_image[new_i, new_j] = image[i, j]

    return scrambled_image

def inverse_enhanced_arnold_cat_map(image):
    height, width = image.shape[:2]
    descrambled_image = np.zeros_like(image)

    for i in range(height):
        for j in range(width):
            old_i = (2 * i - j) % height
            old_j = (i - j) % width
            descrambled_image[old_i, old_j] = image[i, j]

    return descrambled_image

# Path to the zip file containing the DICOM image
zip_file_path = "Image.zip"

# Name of the DICOM file within the zip folder
dicom_filename = "Image.dcm"

# Extract the DICOM file from the zip folder
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract(dicom_filename)

# Load DICOM image from the extracted folder
filename = dicom_filename

try:
    ds = pydicom.dcmread(filename)
    image = ds.pixel_array

    plt.figure(figsize=(10, 10))
    # Display the original image
    plt.subplot(221)
    plt.imshow(image, cmap='gray')
    plt.title('Original DICOM Image')
    plt.axis('off')

    # Scramble the image
    scrambled_image = arnold_cat_map(image)

    # Display the scrambled image
    plt.subplot(222)
    plt.imshow(scrambled_image, cmap='gray')
    plt.title('Scrambled DICOM Image')
    plt.axis('off')

    descrambled_image = inverse_enhanced_arnold_cat_map(scrambled_image)

    # Display the descrambled image
    plt.subplot(223)
    plt.imshow(descrambled_image, cmap='gray')
    plt.title('Descrambled DICOM Image')
    plt.axis('off')

    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
