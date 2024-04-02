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
    """
    Preprocess the DICOM image to discover embeddable blocks using 3-bit MSB prediction.
    """
    def find_combination_with_least_difference(block):
        """
        Find the combination of 3 MSB bits that gives the least difference when subtracted
        from the first pixel of the block.
        """
        predictor_pixel = block[0, 0]
        min_difference = float('inf')
        best_combination = None
        
        # Possible combinations of the 3 MSB bits
        for combination in range(8):
            msb_combination = np.array([combination >> 2 & 1, combination >> 1 & 1, combination & 1])
            difference = np.abs(predictor_pixel - int(''.join(map(str, msb_combination)), 2))
            if difference < min_difference:
                min_difference = difference
                best_combination = msb_combination
        
        return best_combination
    
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
                best_combination = find_combination_with_least_difference(block)
                differences = np.abs(block - int(''.join(map(str, best_combination)), 2))
                
                if np.all(differences <= -64):
                    embeddable_blocks.append(block)
                    mark[y // block_size, x // block_size] = 1
    
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
