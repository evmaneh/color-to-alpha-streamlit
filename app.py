import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
import col_to_alpha as cta

def convert_image(img):
    buf = BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return byte_im

def tuple_to_hex(tup):
    return f'#{tup[0]:02x}{tup[1]:02x}{tup[2]:02x}'.upper()

def hex_to_tuple(hex: str):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def main():
    st.set_page_config(page_title='Color to Alpha', page_icon='', layout='wide')

    st.title('Color to Alpha Algorithms')
    st.write("Upload an image and pick a color.")
    st.markdown("Read more about the algorithm [here](https://medium.com/@mcreynolds02/how-gimps-color-to-alpha-tool-works-82372367afcd).")

    st.sidebar.title('Upload an Image')
    file = st.sidebar.file_uploader('Original image', type=['png', 'jpg', 'jpeg', 'webp'])
    if file is None:
        img = Image.open('colExp.png')
    else:
        img = Image.open(file)

    img = img.convert('RGB')

    st.sidebar.title('Settings :gear:')
    shape = st.sidebar.selectbox('Shape (used for calculating distance in RGB-space)', ['sphere', 'cube'])
    interpolation = st.sidebar.selectbox('Interpolation', ['linear', 'power', 'root', 'smooth', 'inverse-sin'])

    top_threshold_bound = 255 if shape == 'cube' else 442
    transparency_threshold = st.sidebar.slider('Transparency Threshold', 0, top_threshold_bound, 18)
    opacity_threshold = st.sidebar.slider('Opacity Threshold', 0, top_threshold_bound, 193)

    st.sidebar.title('Color Selection')
    color = '#000000'

    color = st.sidebar.color_picker('Color', color)

    col1, col2 = st.columns(2)

    col1.subheader("Original Image 🖼️")
    col1.image(img)

    col2.subheader("Color to Alpha applied :wrench:")
    cta_arr = cta.color_to_alpha(np.array(img), hex_to_tuple(color), transparency_threshold, opacity_threshold, shape=shape, interpolation=interpolation)
    cta_img = Image.fromarray(cta_arr, 'RGBA')

    col2.image(cta_img)

    col2.download_button('Download Image', convert_image(cta_img), file_name='CtA.png', mime='image/png')

if __name__ == '__main__':
    main()
