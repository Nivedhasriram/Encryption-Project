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
    except Exception as e:
        print("Error loading DICOM file:", e)
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
    
    try:
        pixel_data = dicom_image.pixel_array
        np_image = np.array(pixel_data)
        block_size = 8
        height, width = np_image.shape
        embeddable_blocks = []
        mark = np.zeros((height // block_size, width // block_size), dtype=int)
        md5_array = []

        # Find embeddable blocks
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                block = np_image[y:y+block_size, x:x+block_size]
                
                if block.shape == (block_size, block_size):
                    check = find_combination_with_least_difference(block)
                    if check == 1:
                        mark[y // block_size, x // block_size] = 1
                        embeddable_blocks.append(block)

                    md5_hash = hashlib.md5()
                    for row in block:
                        md5_hash.update(bytes(row))
                    md5_value = md5_hash.hexdigest()
                    md5_array.append(md5_value)
                         
        return embeddable_blocks, mark, md5_array
    
    except AttributeError:
        print("AttributeError: Failed to extract pixel data from DICOM image.")
        return None, None, None
    except Exception as e:
        print("Error preprocessing DICOM image:", e)
        return None, None, None

# Example usage:
dicom_path = "Image2.dcm"
dicom_image = input_dicom_image(dicom_path)
if dicom_image:
    embeddable_blocks, mark, md5_array = preprocess_dicom_image(dicom_image)
    if embeddable_blocks is not None:
        print(f"Number of embeddable blocks found: {len(embeddable_blocks)}")
        print("Mark array:")
        print(mark)
        print("MD5 array:")
        for md5_value in md5_array:
            print(md5_value)

# import pydicom
# import numpy as np
# import hashlib

# def input_dicom_image(dicom_path):
#     """
#     Load the DICOM image from the specified path.
#     """
#     try:
#         dicom_image = pydicom.dcmread(dicom_path)
#         return dicom_image
#     except FileNotFoundError:
#         print("DICOM file not found")
#         return None
#     except Exception as e:
#         print("Error loading DICOM file:", e)
#         return None

# def preprocess_dicom_image(dicom_image):
#     def find_combination_with_least_difference(block, y, x):
#         predictor_pixel = block[0, 0]
#         min_difference = float('inf')
#         best_combination = None
#         msb_combinations = np.array([i * 32 for i in range(8)])
#         res = np.zeros((8, 8), dtype=int)  # Initialize res array
        
#         # Possible combinations of the 3 MSB bits
#         for i in range(1, 8):
#             for j in range(1, 8):
#                 actual_pixel = block[i, j]
#                 for value in msb_combinations:
#                     result = actual_pixel ^ value
#                     difference = abs(predictor_pixel - result)
#                     if difference < min_difference:
#                         min_difference = difference
#                         best_combination = value
#                 if best_combination != actual_pixel:
#                     return {
#                         "block": block,
#                         "y": y,
#                         "x": x,
#                         "actual_pixel": actual_pixel
#                     }  # Return the non-embeddable block and its position
                    
#         return None  # If all blocks are embeddable, return None

#     try:
#         pixel_data = dicom_image.pixel_array
#         np_image = np.array(pixel_data)
#         block_size = 8
#         height, width = np_image.shape

#         for y in range(0, height, block_size):
#             for x in range(0, width, block_size):
#                 block = np_image[y:y+block_size, x:x+block_size]
#                 # print(f"Block starting at (y={y}, x={x}):")
#                 # print(block)
                
#                 if block.shape == (block_size, block_size):
#                     block_info = find_combination_with_least_difference(block, y, x)
#                     if block_info is not None:
#                         return block_info
                         
#         print("No non-embeddable block found.")
#         return None
    
#     except AttributeError:
#         print("AttributeError: Failed to extract pixel data from DICOM image.")
#         return None
#     except Exception as e:
#         print("Error preprocessing DICOM image:", e)
#         return None

# # Example usage:
# dicom_path = "Image.dcm"
# dicom_image = input_dicom_image(dicom_path)
# if dicom_image:
#     block_info = preprocess_dicom_image(dicom_image)
#     if block_info is not None:
#         print("Non-embeddable block:")
#         print("Block position (y, x):", block_info["y"], ",", block_info["x"])
#         print("Actual pixel value:", block_info["actual_pixel"])
#         print("Block:")
#         print(block_info["block"])
#         print("Pixel values of the block:")
#         for row in block_info["block"]:
#             print(row)
