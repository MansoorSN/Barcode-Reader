from __future__ import annotations
import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import zxingcpp
import requests
import openfoodfacts


st.set_page_config(page_title="Barcode Reader", layout="wide")



img_file_buffer = st.camera_input("Take a picture")

'''
def find_brocade(r):
    response1=requests.get(f"https://www.brocade.io/api/items/{r.text}")

    if response1:
        
        return response1
    else:
        return None


def find_barcodes_database(r):
    response1=requests.get(f"https://barcodesdatabase.org/barcode/{r.text}")

    if response1:
        
        return response1
    else:
        return None


'''
def openfoodfacts_db(r):
    api = openfoodfacts.API()
    response1= api.product.get(r.text, fields=["product_name_en","ingredients_text_en"])
    
    if response1:
        print("response from open food facts db")
        return response1
    else:
        print("No response from open food facts db")
        return None


#db_dict={1:find_brocade, 2:find_barcodes_database, 3:openfoodfacts_db}
db_dict={1:openfoodfacts_db}

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


        flag=False
        for i in range(1,len(db_dict)+1):
            response=db_dict[i](r)

            if response:
                #st.write(f"The product details for barcode in {response.text}")
                st.write(f"The product details for barcode obtained from {db_dict[i]} in {response}")
                st.write(response)
                flag=True
                break
            
        if flag==False:
            st.write(f"The product for barcode  {r.text} could not be found in the database")




    st.write(results)

    

else:
    st.write("Barcode not found. Please scan again")
