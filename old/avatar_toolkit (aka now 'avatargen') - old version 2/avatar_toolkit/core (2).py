# avatar_toolkit/core.py
"""Core image processing functions for Avatar Toolkit combining face detection and processing."""

import os
import cv2
import numpy as np
from PIL import Image
from avatar_toolkit import face_detect, processing, utils, config
from .config import DEFAULTS

# Load face detection model (OpenCV Haar Cascade)
_face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def process_image(image: Image.Image, config: dict) -> Image.Image:
    """
    Process an input PIL Image according to config and return the resulting Image.
    Operations include face detection and cropping with bezel/mask.
    """
    # Convert PIL Image to OpenCV image (BGR format)
    cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    faces = _face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, 
                                          minSize=(50, 50))
    # Determine crop region (default to center if no face found)
    if len(faces) > 0:
        x, y, w, h = faces[0]  # first detected face
    else:
        # Center crop as fallback
        h, w = gray.shape[:2]
        x, y = w//4, h//4
        w, h = w//2, h//2
    # Crop to face region with some padding (bezel)
    pad = config.get("bezel", DEFAULTS["bezel"])
    x1 = max(x - pad, 0); y1 = max(y - pad, 0)
    x2 = min(x + w + pad, cv_img.shape[1]); y2 = min(y + h + pad, cv_img.shape[0])
    cropped = cv_img[y1:y2, x1:x2]

    # Create rounded-corner mask if specified
    corner = config.get("corner_radius", DEFAULTS["corner_radius"])
    if corner and corner > 0:
        mask = np.zeros(cropped.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (0, 0), (mask.shape[1], mask.shape[0]), 255, -1)
        # Apply a rounded rectangle (using Gaussian blur as approximation)
        mask = cv2.GaussianBlur(mask, (corner, corner), 0)
        for c in range(3):  # apply mask to each channel
            cropped[:, :, c] = cv2.bitwise_and(cropped[:, :, c], cropped[:, :, c], mask=mask)

    # Convert back to PIL Image in RGBA (to preserve transparency if any)
    result_img = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGBA))
    return result_img

def run_single(img: Image.Image, output_path: str, config: dict) -> None:
    """Process and save a single image using the provided configuration."""
    result = process_image(img, config)
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Prepare save parameters
    save_format = config.get("format", DEFAULTS["format"])
    save_kwargs = {"format": save_format}
    if save_format.upper() in ("JPEG", "WEBP"):
        save_kwargs["quality"] = config.get("quality", DEFAULTS.get("quality", 95))
        save_kwargs["optimize"] = True
    result.save(output_path, **save_kwargs)

def generate_avatar(image):
    """
    Generate an avatar (square, resized image) from the input image array.
    :param image: NumPy array (RGB).
    :return: NumPy array of the processed avatar image (RGB).
    """
    # Detect face in the image (if any)
    face_coords = face_detect.detect_face(image)
    # Crop to square region (focused on face if detected)
    cropped = processing.crop_to_square(image, face_coords)
    # Resize to avatar dimensions
    avatar_img = processing.resize_image(cropped, config.AVATAR_SIZE)
    return avatar_img

def generate_avatar_file(input_path, output_path=None):
    """
    Generate an avatar from an input image file, and save to output path.
    :param input_path: Path to input image.
    :param output_path: Path to save output. If None, saves next to input with '_avatar' suffix.
    :return: Path of saved avatar image.
    """
    # Load image using high-performance OpenCV loader:contentReference[oaicite:3]{index=3}
    image = utils.load_image(input_path)
    avatar_img = generate_avatar(image)
    # Determine output path if not specified
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        if ext.lower() not in config.ALLOWED_EXTENSIONS:
            ext = ".png"
        output_path = f"{base}_avatar{ext}"
    # Ensure the output directory exists
    utils.ensure_dir(os.path.dirname(output_path) or ".")
    # Save the avatar image
    utils.save_image(avatar_img, output_path)
    return output_path
