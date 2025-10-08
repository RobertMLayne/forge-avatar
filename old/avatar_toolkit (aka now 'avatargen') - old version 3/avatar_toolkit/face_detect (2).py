from __future__ import annotations

"""
avatar_toolkit/face_detect.py - Face detection utilities.

Responsibilities:
- Detect faces in images
- Crop images to the face or center as needed
"""

__version__ = "1.0.0"
__all__ = ["detect_face", "crop_to_face", "crop_to_face_or_center"]

import cv2
import numpy as np
from PIL import Image


def detect_face(image: Image.Image | np.ndarray) -> tuple[int, int, int, int] | None:
    """Detects the largest face in the image. Returns (x, y, w, h)."""
    # Convert input to numpy array
    if isinstance(image, np.ndarray):
        arr = image
    else:
        arr = np.array(image)
    # Determine image dimensions
    h, w = arr.shape[:2]
    # Convert to grayscale
    if arr.ndim == 3 and arr.shape[2] == 4:
        # RGBA to BGR then to gray
        cv_img = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    elif arr.ndim == 3 and arr.shape[2] == 3:
        gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    else:
        gray = arr

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        # No face detected; return full image bounds
        return (0, 0, w, h)

    # Return the largest face bounding box
    return max(faces, key=lambda r: r[2] * r[3])


def crop_to_face(image: Image.Image, padding: float = 0.25) -> Image.Image:
    """Crops the image to the largest face with optional padding."""
    face_box = detect_face(image)
    if not face_box:
        return image
    x, y, w, h = face_box
    pad_w = int(w * padding)
    pad_h = int(h * padding)

    left = max(0, x - pad_w)
    top = max(0, y - pad_h)
    right = min(image.width, x + w + pad_w)
    bottom = min(image.height, y + h + pad_h)

    return image.crop((left, top, right, bottom))


def crop_to_face_or_center(image: Image.Image) -> Image.Image:
    """Crop to face if detected; otherwise crop center square."""
    face_box = detect_face(image)
    if face_box:
        return crop_to_face(image)
    # No face detected: center crop to square
    w, h = image.width, image.height
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    return image.crop((left, top, left + min_dim, top + min_dim))
