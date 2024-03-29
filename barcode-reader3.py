from __future__ import annotations
import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import zxingcpp
import requests
import openfoodfacts
import pandas as pd


st.set_page_config(page_title="Barcode Reader", layout="wide")
check_list=set(st.secrets['filters']['filter1'])

img_file_buffer = st.camera_input("Take a picture")

def openfoodfacts_db(r):
    api = openfoodfacts.API()
    try:
        response1= api.product.get(r.text)
    except:
        st.write("404: cannot find in Database")
        return None
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
    if len(results)==0:
        st.write("Could not find the barcode, Please scan again")

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

            if r.text.startswith("729"):
                st.markdown('''# :red[Do Not Buy!]''')

            if response:
                #st.write(f"The product details for barcode in {response.text}")
                st.write(f"The product details for barcode obtained from open food facts:")

                df = pd.DataFrame(columns=['Value'], index=['barcode', 'Product Name', 'ingredients', 'brands'])


                if response['code'] is not None:
                  df.loc["barcode"]=response['code']
                else:
                  df.loc["barcode"]=""
                
                
                if 'product_name_en' in response['product']:
                  df.loc["Product Name"]=response['product']['product_name_en']
                elif 'product_name_fr' in response['product']:
                 df.loc["Product Name"]=response['product']['product_name_fr']
                else:
                  df.loc["barcode"]=""
                
                
                if 'ingredients_text_en' in response['product']:
                  df.loc["ingredients"]=response['product']['ingredients_text_en']
                elif 'ingredients_text' in response['product']:
                  df.loc["ingredients"]=response['product']['ingredients_text']
                else:
                  df.loc["barcode"]=""
                
                if 'brands' in response['product']:
                    df.loc["brands"]=response['product']['brands']
                    if df.loc["brands"]["Value"].lower() in check_list:
                        st.markdown('''# :red[Do Not Buy!]''')
                else:
                  df.loc["barcode"]=""
                
                st.table(df)
                st.write()
               
                flag=True
                break
            
        if flag==False:
            st.write(f"The product barcode  {r.text} could not be found in the database")




    #st.write(results)
else:
    st.write("Take a picture of barcode")
