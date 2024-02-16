"""Style transfer."""
from argparse import ArgumentParser
from torchvision import transforms
from tqdm import tqdm
from datetime import datetime
import torch
import os
import re
from PIL import Image

import src.utils.images_utils as iu
from src.networks.image_transformer_net import ImageTransformNet


def style_transfer(image: Image.Image, device: torch.device, model: torch.nn.Module, img_size: int = 180) -> Image.Image:
    """
    Apply style transfer to the input image using the given model.

    Parameters:
    - image (PIL.Image.Image): The original image.
    - device (torch.device): The device on which to perform the style transfer (e.g., 'cuda' for GPU or 'cpu').
    - model (torch.nn.Module): The pre-trained style transfer model.
    - img_size (int): The size of the output image. Default is 180.

    Returns:
    - PIL.Image.Image: The stylized image.
    """

    # Preprocess image
    image_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),          # Scale shortest side to image_size
        transforms.CenterCrop(img_size),                  # Crop center image_size out
        transforms.ToTensor(),                            # Turn image from [0-255] to [0-1]
        transforms.Normalize(mean=iu.IMAGENET_MEAN,
                             std=iu.IMAGENET_STD)            # Normalize with ImageNet values
    ])

    image = image_transform(image).unsqueeze(0).to(device)

    # Perform style transfer
    image = model(image).cpu().data[0]

    # Denormalize the output image
    image = iu.denormalize_image(image)

    return image


def folder_style_transfer(args:ArgumentParser) -> None :
    """
    Uses an already trained model to perform style transfer over some base images.

    Parameters
    ----------
    args : ArgumentParser
        arguments passed through a terminal. Here is the list of arguments:
            
            args.model-path : a str. The path leading to the trained model to use.
            args.source: a str. The path to the folder containing the images to stylize. Many images can be transformed at once.
            args.output: a str. The path where the stylized images will be saved.
            args.image-size: a float. The size (both height and width: if the image is not squared, it will be after the transform) of the output image

    Returns
    -------
    None. Everything is done inside the function.

    """
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    style_model = ImageTransformNet().to(device) # loads the image transformation network and sends it to the device.
    style_model.load_state_dict(torch.load(args.model_path, map_location=device)) # loads the weights of the desired model.

    pattern = re.compile(r"\/([a-zA-Z_]+)_\d+_epochs_\d+_samples_\d+_\d+\.\d+_cttwght\.model")
    model_name = pattern.search(args.model_path).group(1)
    output_dir = os.path.join(args.output, model_name)

    if not os.path.exists(output_dir): # checks if the output directory exists. If not, creates it.
        os.makedirs(output_dir)

    start = datetime.now()
    count = 0
    for img_fn in tqdm(os.listdir(args.source), desc="Stylizing images"): # stylize all images present in the source directory.
        img_path = os.path.join(args.source, img_fn)
        content = iu.load_image(img_path)
        stylized = style_transfer(content, device, style_model, args.image_size)
        out_im_fn = f"{model_name}_{img_fn}"
        iu.save_image(os.path.join(output_dir, out_im_fn), stylized, denormalize=False)
        count += 1

    print(f"Average inference time : {(datetime.now() - start) / count}")

if __name__ == '__main__':
    parser = ArgumentParser(description='Apply a style to an image.')

    parser.add_argument(
        "--model_path",
        type=str,
        required=True,
        help="Path to the desired style model.")
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to the folder containing images to transform.")
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path where to save the stylized images.")
    parser.add_argument(
        "--image-size",
        type=int,
        default=256,
        help="Size of the input images (both width and height).")

    args = parser.parse_args()
    folder_style_transfer(args)
