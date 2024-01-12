import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import zxingcpp


img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # To read image file buffer as a 3D uint8 tensor with TensorFlow:

    barcode_image = Image.open(img_file_buffer)
    results = zxingcpp.read_barcodes(barcode_image)

    for r in results:
        print(f"Text:          '{r.text}'")
        print(f"Symbology:     {r.format.name}")
        print(f"Content Type:  {r.content_type.name}")
        print(f"Bounding Box:  {r.position}")
        print(f"Rotation:      {r.orientation}deg")
        print("---")

        st.write(f"Text:          '{r.text}'")
        st.write(f"Symbology:     {r.format.name}")
        st.write(f"Content Type:  {r.content_type.name}")
        st.write(f"Bounding Box:  {r.position}")
        st.write(f"Rotation:      {r.orientation}deg")


        response=requests.get(f"https://www.brocade.io/api/items/{r.text}")

        if response:
            st.write(f"The product details for barcode in {r.text}")
            st.write(response.text)
        else:
            st.write(f"The product for barcode  {r.text} could not be found in the database")



    st.write(results)
    
else:
    st.write("No Barcode found")
