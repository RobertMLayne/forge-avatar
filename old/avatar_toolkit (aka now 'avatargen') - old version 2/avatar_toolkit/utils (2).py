"""Utility functions for image loading, saving, and conversions."""
import os
import re
import cv2
from pathlib import Path
from typing import Optional
from PIL import Image
import numpy as np


def slugify(text: str) -> str:
    """Converts text to a filesystem-safe slug."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text).strip('_').lower()


def ensure_dir(path: str | Path) -> None:
    """Creates the directory if it does not exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


def infer_output_filename(input_path: str | Path, suffix: str = "_out", ext: Optional[str] = None) -> str:
    """Generates an output filename by appending a suffix to the stem."""
    p = Path(input_path)
    new_ext = ext if ext else p.suffix
    return str(p.with_name(p.stem + suffix).with_suffix(new_ext))


def is_image_file(path: str | Path) -> bool:
    """Checks if the file has a known image extension."""
    return Path(path).suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'}


def load_image(path: str):
    """Load an image from file path as an RGB NumPy array."""
    # Use OpenCV to load image (faster than PIL for image reading:contentReference[oaicite:2]{index=2})
    img_bgr = cv2.imread(path)
    if img_bgr is None:
        raise FileNotFoundError(f"Image file not found: {path}")
    # Convert BGR (OpenCV default) to RGB color format
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_rgb

def save_image(image, path: str):
    """Save an image (NumPy array or PIL Image) to file at given path."""
    # If image is a PIL Image, convert to array
    if isinstance(image, Image.Image):
        image = image.convert("RGB")
        image = np.array(image)
    # Convert from RGB to BGR for OpenCV before saving
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, image_bgr)

def cv_to_pil(image):
    """Convert a NumPy RGB image array to a PIL Image."""
    return Image.fromarray(image)

def ensure_dir(dir_path: str):
    """Ensure that a directory exists."""
    os.makedirs(dir_path, exist_ok=True)
