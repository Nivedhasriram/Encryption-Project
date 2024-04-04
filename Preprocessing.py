import pydicom
import numpy as np
import hashlib

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

def preprocess_dicom_image(dicom_image):
    def find_combination_with_least_difference(block):
        predictor_pixel = block[0, 0]
        min_difference = float('inf')
        best_combination = None
        msb_combinations = np.array([i * 32 for i in range(8)])
        res = np.zeros((8, 8), dtype=int)  # Initialize res array
        
        # Possible combinations of the 3 MSB bits
        for i in range(1, 8):
            for j in range(1, 8):
                actual_pixel = block[i, j]
                for value in msb_combinations:
                    result = actual_pixel ^ value
                    difference = abs(predictor_pixel - result)
                    if difference < min_difference:
                        min_difference = difference
                        best_combination = value
                if best_combination != actual_pixel:
                    return 0  # Return immediately if a mismatch is found
                else:
                    res[i, j] = 1
                    
        return 1  # If no mismatches found, return 1
    
    pixel_data = dicom_image.pixel_array
    np_image = np.array(pixel_data)
    block_size = 8
    height, width = np_image.shape
    embeddable_blocks = []
    mark = np.zeros((height // block_size, width // block_size), dtype=int)
    
    # find embeddable blocks
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = np_image[y:y+block_size, x:x+block_size]
            
            if block.shape == (block_size, block_size):
                check = find_combination_with_least_difference(block)
                if check == 1:
                    mark[y // block_size, x // block_size] = 1
                    embeddable_blocks.append(block)
                     
    return embeddable_blocks, mark

    

# Example usage:
dicom_path = "Image.dcm"
dicom_image = input_dicom_image(dicom_path)
if dicom_image:
    embeddable_blocks, mark = preprocess_dicom_image(dicom_image)
    print(f"Number of embeddable blocks found: {len(embeddable_blocks)}")
    print("Mark array:")
    print(mark)

#MD5 CALCULATION 
# def generate_md5_hash(block):
#     """
#     Generate MD5 hash for a given block.
#     """
#     block_bytes = block.tobytes()
#     md5_hash = hashlib.md5(block_bytes).hexdigest()
#     return md5_hash

# # Example usage:
# block = embeddable_blocks[0]  # Assuming we have embeddable blocks from previous step
# md5_hash = generate_md5_hash(block)
# print(f"MD5 hash for the block: {md5_hash}")
