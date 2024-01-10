import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from pyzbar.pyzbar import decode
#picture = st.camera_input("Take a picture")

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # To read image file buffer as a 3D uint8 tensor with TensorFlow:
  
    
    barcode_image = Image.open(img_file_buffer)

    # Decode the barcode
    decoded_objects = decode(barcode_image)

    # Print the barcode data (if any)
    if decoded_objects:
        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')
            barcode_type = obj.type
            st.write(f"Barcode Type: {barcode_type}, Data: {barcode_data}")
    else:
        st.write("No barcode found in the image.")
        