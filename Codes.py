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
from pydicom.pixel_data_handlers.util import apply_voi_lut
import zipfile
import os

def extract_dicom_from_zip(zip_file_path, output_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

def load_dicom_with_voi_lut(dicom_path):
    dicom_data = pydicom.dcmread(dicom_path)
    img = apply_voi_lut(dicom_data.pixel_array, dicom_data)
    return img

def blockshaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h // nrows, nrows, -1, ncols)
               .swapaxes(1, 2)
               .reshape(-1, nrows, ncols))

def xor_scramble(image_array, block_size):
    image_blocks = blockshaped(image_array, block_size, block_size)
    random_matrix = np.random.randint(0, 256, size=image_blocks.shape, dtype=np.uint8)
    xor_result_blocks = np.bitwise_xor(image_blocks, random_matrix)
    xor_result = xor_result_blocks.reshape(image_array.shape)
    return xor_result

zip_file_path = "Image_scrambled.zip"
output_dir = "./extracted_dicom"

extract_dicom_from_zip(zip_file_path, output_dir)

dicom_filename = "Image_scrambled.dcm"
dicom_path = os.path.join(output_dir, dicom_filename)

dicom_data = pydicom.dcmread(dicom_path)
img_with_voi_lut = load_dicom_with_voi_lut(dicom_path)

block_size = 8
scrambled_image = xor_scramble(img_with_voi_lut, block_size)
xor_image = Image.fromarray(scrambled_image)
xor_image.show()

