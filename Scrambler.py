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
            new_i = (i + j) % height
            new_j = (i + 2 * j) % width
            scrambled_image[new_i, new_j] = image[i, j]

    return scrambled_image

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

    # Display the original image
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original DICOM Image')
    plt.axis('off')

    # Scramble the image
    scrambled_image = arnold_cat_map(image)

    # Display the scrambled image
    plt.subplot(1, 2, 2)
    plt.imshow(scrambled_image, cmap='gray')
    plt.title('Scrambled DICOM Image')
    plt.axis('off')

    plt.show()

except Exception as e:
    print("An error occurred:", str(e))
