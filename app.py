"""App that applies style transfer to an image uploaded by a user."""

import os
from io import BytesIO
import requests
import streamlit as st
from streamlit_image_select import image_select
from PIL import Image
import torch

from src.networks.image_transformer_net import ImageTransformNet
from src.models.style_transfer import style_transfer
from src.utils.get_yaml_config import import_yaml_config


def page_intro():
    """Style and introduction of the page."""
    st.set_page_config(
        page_title="Style transfer", page_icon="🖼️", initial_sidebar_state="collapsed"
    )
    
    st.title(
        ":rainbow[Add a new style to your pictures]"
    )

    st.write(
        """
        Style transfer is a deep learning task, that lets you merge the style of one image with the content of another. 
        Our app offers three distinct styles to transform your photos. 
        Simply select a style, upload a picture of your choice, and watch as the app transforms your image!
        """
            )


def display_styles(styles_path="static/styles"):
    """Display the different styles and allow the user to select one."""

    # Create a dictionnary with the different styles names and the paths to the corresponding images
    styles = {}
    for style in os.listdir(styles_path):
        styles[style.split(".")[0]] = f"{styles_path}/{style}"

    # Display the styles to choose from
    styles_names = [name.replace("_", " ").title() for name in list(styles.keys())]

    st.subheader("Our styles :frame_with_picture:")
    selected_style_index = image_select(label="First, choose one of the following styles:", 
                                  images=list(styles.values()),
                                  captions=styles_names,
                                  index=0,
                                  return_value="index"
                                  )
    
    # Return the selected style (mosaic, tapestry or starry_night)
    selected_style = list(styles.keys())[selected_style_index]

    return selected_style


def upload_image():
    """Display a box in which the user can upload an image."""

    st.subheader("Your photo :camera_with_flash:")

    # File uploader widget for image upload
    uploaded_image = st.file_uploader("Then, upload a picture:", type=["jpg", "png"])

    return uploaded_image


@st.cache_data
def torch_device():
    """Set torch device for style transfer models"""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@st.cache_data
def load_model(model_path, device):
    """Load the specified style transfer model."""

    response = requests.get(model_path, timeout=30)
    model_bytes = BytesIO(response.content)

    # Load the image transformation network and sends it to the device.
    style_model = ImageTransformNet().to(device)

    # Load the weights of the desired model.
    style_model.load_state_dict(torch.load(model_bytes, map_location=device))

    return style_model


def transform_image(image, device, model):
    """Apply style transfer to the image."""
    image = Image.open(image)

    # Convert image to RGB (3 channels)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize images that are too large (max length=1500)
    if any(element > 1500 for element in image.size):
        image.thumbnail((1500, 1500))

    size = image.size
    image = style_transfer(image, device, model, img_size=max(size))
    image = image.resize(size)
    return image


def display_transformed_image(original_image, transformed_image):
    """Display the original and the transformed images."""

    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        st.image(original_image, caption="Original image", use_column_width=True)

    with col2:
        st.image(transformed_image, caption="Transformed image", use_column_width=True)


def download_transformed_image(image):
    """Allows the user to download the transformed image."""

    # Convert the PIL image to bytes
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)  # Reset the file pointer to the beginning

    # Create the download button
    st.download_button(label="Download your image!",
                           data=image_bytes,
                           file_name="style_transfer_image.jpg",
                           mime="image/jpeg"  
                           )



def main(models_path):
    """
    Execute the app code (style selection and image upload by the user,
    style transfer, result display)
    """

    page_intro()
    device = torch_device()
    style = display_styles()
    model = load_model(f"{models_path}/{style}.model", device)
    image = upload_image()

    st.subheader("The transformation :sparkles:")

    if image is not None:
        transformed_image = transform_image(image, device, model)
        display_transformed_image(image, transformed_image)
        download_transformed_image(transformed_image)

    else:
        st.info("Waiting for an image to transform...")


if __name__ == "__main__":
    config = import_yaml_config()
    models_folder = config.get(
        "models_folder",
        "https://minio.lab.sspcloud.fr/mbricaire/mise-en-production/models",
    )
    main(models_path=models_folder)
