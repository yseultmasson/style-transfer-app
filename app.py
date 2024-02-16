import streamlit as st
import os
from PIL import Image


def display_styles(styles_path='static/styles'):
    st.title('Choose one of the following styles')

    # Create a dictionnary with the different styles names and the paths to the corresponding images
    styles = {}
    for style in os.listdir(styles_path):
        styles[style.split('.')[0]] = f'{styles_path}/{style}'

    # Display the box to choose a style
    selected_image = st.selectbox('Select an image:', list(styles.keys()))

    # Display the selected image
    st.image(styles[selected_image], caption=selected_image, width=256)


def upload_image():
    # File uploader widget for image upload
    uploaded_image = st.file_uploader('Upload an image:', type=['jpg', 'jpeg', 'png'])

    if uploaded_image is None:
        st.info('Please upload an image.')

    return uploaded_image


def transform_image(image):
    image = Image.open(image)
    return image.convert('1')


def display_transformed_image(original_image, transformed_image):
    # Display the original and the transformed images side by side
    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        st.image(original_image, caption='Original image', use_column_width=True)

    with col2:
        st.image(transformed_image, caption='Transformed image', use_column_width=True)

if __name__ == "__main__":
    display_styles()
    image = upload_image()
    if image is not None:
        transformed_image = transform_image(image)
        display_transformed_image(image, transformed_image)
