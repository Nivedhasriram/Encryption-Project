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
scrambled_image_path = dicom_filename
scrambled_dicom = pydicom.dcmread(scrambled_image_path)

# Apply VOI LUT transformation
scrambled_img = scrambled_dicom.pixel_array
if 'VOILUTFunction' in scrambled_dicom:
    lut_function = int(scrambled_dicom.VOILUTFunction)
    if lut_function == 1:
        scrambled_img = apply_voi_lut(scrambled_img, scrambled_dicom)

# Define the inverse Arnold's cat map function
def inverse_arnold_cat_map(image, iterations):
    height, width = image.shape
    assert height == width, "Image should be square"
    assert height % 2 == 0, "Image size should be even"
    inverse_transformation_matrix = np.array([[1, -1], [-1, 2]])

    for i in range(iterations):
        for x in range(height):
            for y in range(width):
                old_pos = np.array([x, y])
                new_pos = np.dot(inverse_transformation_matrix, old_pos) % height
                image[x, y] = image[new_pos[0], new_pos[1]]
    return image

# Descramble the image
descrambled_img = inverse_arnold_cat_map(scrambled_img, 10)

# Create a new DICOM object for the descrambled image
descrambled_dicom = pydicom.dcmread(scrambled_image_path)
descrambled_dicom.PixelData = descrambled_img.tobytes()

# Display the descrambled image
plt.imshow(descrambled_img, cmap='gray')
plt.title('Descrambled Image')
plt.axis('off')
plt.show()


