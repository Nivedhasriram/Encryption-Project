# import random
# import os
# import pydicom
# from PIL import Image
# import numpy as np

import os
import random
import pydicom
import numpy as np

def encrypt_dicom_image(password, filename, file_destination):
    try:
        ds = pydicom.dcmread(filename)
        pixelList = ds.pixel_array.flatten()
        random.seed(password)
        random.shuffle(pixelList)
        ds_encrypted = ds.copy()
        ds_encrypted.PixelData = pixelList.tobytes()
        encrypted_filename = os.path.join(file_destination, f"encrypted_{os.path.basename(filename)}")
        ds_encrypted.save_as(encrypted_filename)
        print("DICOM image encrypted and saved as:", encrypted_filename)
        return encrypted_filename
    except Exception as e:
        print("Error occurred during encryption:", str(e))
        return None

def decrypt_dicom_image(password, filename, file_destination):
    try:
        ds_encrypted = pydicom.dcmread(filename)
        pixelList = np.frombuffer(ds_encrypted.PixelData, dtype=np.uint16)
        indexVal = list(range(len(pixelList)))
        random.seed(password)
        random.shuffle(indexVal)
        NewPixelList = np.zeros_like(pixelList)
        for i, j in enumerate(indexVal):
            NewPixelList[j] = pixelList[i]
        ds_decrypted = ds_encrypted.copy()
        ds_decrypted.PixelData = NewPixelList.tobytes()
        decrypted_filename = os.path.join(file_destination, f"decrypted_{os.path.basename(filename)}")
        ds_decrypted.save_as(decrypted_filename)
        print("DICOM image decrypted and saved as:", decrypted_filename)
        return decrypted_filename
    except Exception as e:
        print("Error occurred during decryption:", str(e))
        return None
    
password = "your_password"

# Assuming the DICOM file is named "Image.dcm" and is in the same directory as this code file
filename = "Image.dcm"

# Replace 'file_destination' with the directory where you want to save the encrypted/decrypted DICOM image
file_destination = ""

# Encrypt DICOM image
encrypted_filename = encrypt_dicom_image(password, filename, file_destination)

if encrypted_filename:
    # Decrypt DICOM image
    decrypted_filename = decrypt_dicom_image(password, encrypted_filename, file_destination)

# def encrypt_image(password, filename, file_destination):
#     im = Image.open("/1.decrypted0.png")
#     pixelList = list(im.getdata())
#     random.seed(password)
#     random.shuffle(pixelList)
#     img = Image.new(im.mode, im.size)
#     img.putdata(pixelList)
#     encrypted_filename = os.path.join(file_destination, f"encrypted_{os.path.basename(filename)}")
#     img.save(encrypted_filename)
#     im.close()
#     img.close()
#     return encrypted_filename

# def decrypt_image(password, filename, file_destination):
#     im = Image.open(filename)
#     pixelList = list(im.getdata())
#     indexVal = list(range(len(pixelList)))
#     random.seed(password)
#     random.shuffle(indexVal)
#     NewPixelList = [0] * (im.size[0] * im.size[1])
#     for i, j in enumerate(indexVal):
#         NewPixelList[j] = pixelList[i]
#     out = Image.new(im.mode, im.size)
#     out.putdata(NewPixelList)
#     decrypted_filename = os.path.join(file_destination, f"decrypted_{os.path.basename(filename)}")
#     out.save(decrypted_filename)
#     im.close()
#     out.close()
#     return decrypted_filename

# def encrypt_dicom_image(password, filename, file_destination):
#     ds = pydicom.dcmread(filename)
#     pixelList = ds.pixel_array.flatten()
#     random.seed(password)
#     random.shuffle(pixelList)
#     ds_encrypted = ds.copy()
#     ds_encrypted.PixelData = pixelList.tobytes()
#     encrypted_filename = os.path.join(file_destination, f"encrypted_{os.path.basename(filename)}")
#     ds_encrypted.save_as(encrypted_filename)
#     return encrypted_filename

# def decrypt_dicom_image(password, filename, file_destination):
#     ds_encrypted = pydicom.dcmread(filename)
#     pixelList = np.frombuffer(ds_encrypted.PixelData, dtype=np.uint16)
#     indexVal = list(range(len(pixelList)))
#     random.seed(password)
#     random.shuffle(indexVal)
#     NewPixelList = np.zeros_like(pixelList)
#     for i, j in enumerate(indexVal):
#         NewPixelList[j] = pixelList[i]
#     ds_decrypted = ds_encrypted.copy()
#     ds_decrypted.PixelData = NewPixelList.tobytes()
#     decrypted_filename = os.path.join(file_destination, f"decrypted_{os.path.basename(filename)}")
#     ds_decrypted.save_as(decrypted_filename)
#     return decrypted_filename

# filename = "Image.dcm"
# password = "your_password"
# file_destination = "./Image-Encryption-with-Image-Scrambler"