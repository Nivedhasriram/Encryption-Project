# Arnold code 
# import numpy as np
# import matplotlib.pyplot as plt
# from numba import njit
# import pydicom
# import os
# import zipfile

# @njit()
# def arnold_cat_map(image):
#     height, width = image.shape[:2]
#     scrambled_image = np.zeros_like(image)

#     for i in range(height):
#         for j in range(width):
#             new_i = (i + 2 * j) % height  # Modify the row index calculation
#             new_j = (i + 3 * j) % width   # Modify the column index calculation
#             scrambled_image[new_i, new_j] = image[i, j]

#     return scrambled_image

# def inverse_enhanced_arnold_cat_map(image):
#     height, width = image.shape[:2]
#     descrambled_image = np.zeros_like(image)

#     for i in range(height):
#         for j in range(width):
#             old_i = (2 * i - j) % height
#             old_j = (i - j) % width
#             descrambled_image[old_i, old_j] = image[i, j]

#     return descrambled_image

# zip_file_path = "Image.zip"
# dicom_filename = "Image.dcm"

# with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#     zip_ref.extract(dicom_filename)

# filename = dicom_filename

# try:
#     ds = pydicom.dcmread(filename)
#     image = ds.pixel_array

#     plt.figure(figsize=(10, 10))
#     # Display the original image
#     plt.subplot(221)
#     plt.imshow(image, cmap='gray')
#     plt.title('Original DICOM Image')
#     plt.axis('off')

#     scrambled_image = arnold_cat_map(image)

#     plt.subplot(222)
#     plt.imshow(scrambled_image, cmap='gray')
#     plt.title('Scrambled DICOM Image')
#     plt.axis('off')

#     descrambled_image = inverse_enhanced_arnold_cat_map(scrambled_image)

#     plt.subplot(223)
#     plt.imshow(descrambled_image, cmap='gray')
#     plt.title('Descrambled DICOM Image')
#     plt.axis('off')

#     plt.show()

# except Exception as e:
#     print("An error occurred:", str(e))


#checking bit size of image 
import zipfile
import pydicom

def check_dicom_bit_depth(dicom_data):
    bits_allocated = dicom_data.BitsAllocated
    print(f"The DICOM image is {bits_allocated}-bit.")

zip_file_path = "Image.zip"
dicom_filename = "Image.dcm"
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract(dicom_filename)

dicom_path = dicom_filename
dicom_data = pydicom.dcmread(dicom_path)

check_dicom_bit_depth(dicom_data)


#Psudeo random matrix 

import numpy as np

np.random.seed(42)
matrix = np.random.randint(0, 2**16, size=(512, 512))
print(matrix)

#Pixel value for range 
import zipfile
import pydicom

def check_dicom_pixel_value_and_range(dicom_data):
    # Access a pixel value at a specific location (e.g., row=100, column=200)
    row = 0
    column = 0
    pixel_value = dicom_data.pixel_array[row, column]
    print("Pixel value at (row={}, column={}): {}".format(row, column, pixel_value))

    # Find the value range of the DICOM image
    min_value = dicom_data.pixel_array.min()
    max_value = dicom_data.pixel_array.max()
    print("Minimum pixel value: {}".format(min_value))
    print("Maximum pixel value: {}".format(max_value))

zip_file_path = "Image.zip"
dicom_filename = "Image.dcm"

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract(dicom_filename)

dicom_path = dicom_filename
dicom_data = pydicom.dcmread(dicom_path)
check_dicom_pixel_value_and_range(dicom_data)

#Xor scrambling 
import numpy as np
from PIL import Image
import pydicom
import zipfile
import os

zip_file_path = "Image_scrambled.zip"

# Extract DICOM file from the zip archive
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall()

dicom_filename = "Image_scrambled.dcm"

# Load DICOM file
dicom_path = os.path.join(os.getcwd(), dicom_filename)
dicom_data = pydicom.dcmread(dicom_path)

# Extract pixel data from DICOM
image_array = dicom_data.pixel_array

# Function to divide the image into blocks of size (block_size x block_size)
def blockshaped(arr, nrows, ncols):
    """
    Returns an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array looks like 3D
    """
    h, w = arr.shape
    return (arr.reshape(h // nrows, nrows, -1, ncols)
               .swapaxes(1, 2)
               .reshape(-1, nrows, ncols))

block_size = 8
image_blocks = blockshaped(image_array, block_size, block_size)

# Generate a pseudo-random matrix of the same size as image_blocks
random_matrix = np.random.randint(0, 256, size=image_blocks.shape, dtype=np.uint8)

# Perform XOR operation between each block of the image and the random matrix
xor_result_blocks = np.bitwise_xor(image_blocks, random_matrix)

# Reshape the result back to the original shape
xor_result = xor_result_blocks.reshape(image_array.shape)

# Convert the result back to an image
xor_image = Image.fromarray(xor_result)

# Display the XORed image
xor_image.show()
