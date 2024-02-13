"""Useful constants and functions for images."""
from PIL import Image
import numpy as np

# useful constants
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def load_image(filename:str):
    """
    Opens and returns an image from a filename. It is returned as a PIL image, with RGB values ranging from 0 to 255.

    Parameters
    ----------
    filename : str
        The name of the input file.

    Returns
    -------
    img : Image

    """
    img = Image.open(filename)
    return img

def save_image(filename:str, data:Image) -> None:
    """
    Saves an image, assuming its data comes in batch form (channels, height, width)

    Parameters
    ----------
    filename : str
        The name of the output file.
    data : tensor
        image as a tensor of shape (channels, height, width).

    Returns
    -------
    None. Everything is done inside the function.

    """
    mean = np.array(IMAGENET_MEAN).reshape((3, 1, 1))
    std = np.array(IMAGENET_STD).reshape((3, 1, 1))
    img = data.clone().numpy()
    img = ((img * std + mean).transpose(1, 2, 0) * 255.0).clip(0, 255).astype("uint8")
    img = Image.fromarray(img)
    img.save(filename)
