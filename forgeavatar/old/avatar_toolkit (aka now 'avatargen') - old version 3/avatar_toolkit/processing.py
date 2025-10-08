from __future__ import annotations

"""
avatar_toolkit/processing.py - Image processing routines.

Responsibilities:
- Create masks and bezels for images
- Core image processing pipeline
"""

__version__ = "1.0.0"
__all__ = [
    "create_circular_mask",
    "create_dual_bezel",
    "process_image",
]

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


def create_circular_mask(size: int, border: int, radius: int) -> Image.Image:
    """Create a circular mask of given size with specified border."""
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    # Draw an ellipse filling the inner area
    draw.ellipse((border, border, size - border, size - border), fill=255)
    return mask


def create_dual_bezel(size: int, bezel: int, color1: str, color2: str, radius: int) -> Image.Image:
    """Create an image with dual-color bezel (border) for given size."""
    bezel_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bezel_img)
    # Outer bezel
    outer_bbox = (0, 0, size - 1, size - 1)
    draw.ellipse(outer_bbox, outline=color1, width=bezel)
    # Inner bezel
    inner_bbox = (bezel, bezel, size - 1 - bezel, size - 1 - bezel)
    draw.ellipse(inner_bbox, outline=color2, width=bezel)
    return bezel_img


def process_image(image: Image.Image | str, config: dict[str, object]) -> Image.Image:
    """Apply processing steps to an image according to config."""
    # Open image if a path is provided
    if isinstance(image, (str, Path)):
        image = Image.open(image).convert("RGBA")  # type: ignore

    # Ensure RGBA mode
    img = image.convert("RGBA")
    width = config.get("width", 0)
    height = config.get("height", 0)

    # Face detection crop
    if config.get("face_detect"):
        from .face_detect import detect_face

        box = detect_face(img)
        if box:
            x, y, w, h = box
            img = img.crop((x, y, x + w, y + h))

    # Resize according to retina scale
    retina = config.get("retina_scale", 1)
    target_w = int(width * retina)
    target_h = int(height * retina)
    if target_w > 0 and target_h > 0:
        img = img.resize((target_w, target_h), Image.LANCZOS)

    # Grayscale if requested
    if config.get("grayscale"):
        img = img.convert("L").convert("RGBA")

    # Note: Additional processing like drop shadow can be added here

    return img
