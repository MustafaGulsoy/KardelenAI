import base64
import io
import os
import tempfile
import wave

import cv2
import numpy as np
import pydicom
import requests
from PIL import Image
from PIL import ImageSequence


def base64_to_cv2_img(base64_string):
    if 'base64,' in base64_string:
        base64_string = base64_string.split('base64,')[1]
    img_data = base64.b64decode(base64_string)
    np_arr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


def base64_to_wav(base64_string):
    # Decode the base64 string
    wav_data = base64.b64decode(base64_string)

    # Open a new WAV file for writing
    with wave.open('C:/Projeler/Bussines/KardelenYazilim/Projeler/Python/KardelenAI/Commons/Resources/test.wav',
                   'wb') as wav_file:
        # Set the WAV file parameters
        # You may need to adjust these based on your specific audio data
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
        wav_file.setframerate(44100)  # Sample rate (e.g., 44.1 kHz)

        # Write the audio data to the WAV file
        wav_file.writeframes(wav_data)


def wav_to_base64(file_path):
    # Open the .wav file in binary mode
    with open(file_path, 'rb') as file:
        # Read the file content as binary
        file_content = file.read()

    # Encode the binary data to Base64
    base64_encoded = base64.b64encode(file_content)

    # Convert Base64 bytes to a string (optional)
    base64_string = base64_encoded.decode('utf-8')

    return base64_string


def get_num_channels_from_byte_data(byte_data):
    # Geçici bir dosya oluşturun
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav_file:
        temp_wav_file.write(byte_data)
        temp_wav_file_path = temp_wav_file.name

    # Geçici dosyayı açıp analiz edin
    try:
        with wave.open(temp_wav_file_path, 'rb') as wav_file:
            num_channels = wav_file.getnchannels()
            return num_channels
    finally:
        # Geçici dosyayı silin
        os.remove(temp_wav_file_path)


def convert_pacs_to_png(input_file):
    # Read the DICOM file
    dicom = pydicom.dcmread(input_file)

    # Get pixel data
    img = dicom.pixel_array

    # Normalize the image
    if img.dtype != np.uint8:
        img = img.astype(float)
        img = (img - img.min()) / (img.max() - img.min())
        img = (img * 255).astype(np.uint8)

    return img


def convert_to_png_from_url(url, header):
    file_type = url.split('.')[-1].split('/')[-1].lower().strip()

    response = requests.get(url, headers=header)

    if file_type in ['*','jpg', 'jpeg', 'png', 'webp', 'tga', 'bmp']:
        return convert_image_to_png(response.content)
    elif file_type in ['gif', 'tiff']:
        return convert_gif_tiff_to_array(response.content)
    elif file_type == 'dicom':
        return convert_dicom_to_png(response.content)
    # elif file_type == 'octet-stream':
    #     convert_pxd_to_opencv_array(response.content)
    else:
        raise ValueError(f"File type {file_type} is not supported.")


def convert_image_to_png(file_bytes):
    np_array = np.frombuffer(file_bytes, np.uint8)

    # Step 3: Decode the image using OpenCV
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return [image]


def convert_dicom_to_png(file_bytes):
    # Step 1: Read the DICOM file
    dicom_data = pydicom.dcmread(io.BytesIO(file_bytes))

    # Step 2: Get the pixel array from the DICOM data
    dicom_image = dicom_data.pixel_array

    # Step 3: Convert the pixel array to a PIL Image
    img = Image.fromarray(dicom_image)

    # Step 4: Convert the PIL Image to an RGB image
    img_rgb = img.convert('RGB')

    # Step 5: Convert the PIL Image to a NumPy array
    np_image = np.array(img_rgb)

    # Step 6: Convert the RGB image to BGR format for OpenCV
    img_bgr = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

    return [img_bgr]


def convert_gif_tiff_to_array(file_bytes):
    """
    Convert GIF or TIFF image bytes to a list of NumPy arrays suitable for OpenCV processing.

    Parameters:
    - file_bytes: Byte array of the GIF or TIFF image.

    Returns:
    - A list of NumPy arrays representing image frames in BGR format.
    """
    # Convert byte array to PIL Image
    pil_image = Image.open(io.BytesIO(file_bytes))

    frames = []
    for frame in ImageSequence.Iterator(pil_image):
        # Convert frame to RGB mode if necessary
        frame = frame.convert('RGB')

        # Convert the PIL Image to PNG format in memory
        with io.BytesIO() as buffer:
            frame.save(buffer, format='PNG')
            buffer.seek(0)
            np_array = np.frombuffer(buffer.read(), np.uint8)

        # Decode PNG image using OpenCV
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        frames.append(image)

    return frames

