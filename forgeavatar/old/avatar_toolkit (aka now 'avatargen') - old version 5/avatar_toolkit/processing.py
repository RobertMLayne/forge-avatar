from __future__ import annotations

"""avatar_toolkit/processing.py - Image processing routines.

Responsibilities:
• Create circular masks and apply bezels to images
• Core image processing pipeline for avatar generation
"""
__version__ = "1.0.0"
__all__ = [
    "create_circular_mask",
    "create_dual_bezel",
    "process_image",
]

import logging
from PIL import Image, ImageDraw, ImageFilter

logger = logging.getLogger(__name__)

def create_circular_mask(width: int, height: int) -> Image.Image:
    """Create a circular mask for an image of given width and height."""
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    return mask

def create_dual_bezel(width: int, height: int, bezel: int) -> Image.Image:
    """Create a bezel mask: transparent border with size bezel."""
    mask = Image.new("L", (width, height), 255)
    if bezel > 0:
        draw = ImageDraw.Draw(mask)
        draw.ellipse(
            (bezel, bezel, width - bezel, height - bezel),
            fill=0
        )
    return mask

def process_image(img: Image.Image, config: dict) -> Image.Image:
    """Apply mask, bezels, and other effects to create an avatar image."""
    width, height = img.size
    output = Image.new("RGBA", (width, height))

    mask = create_circular_mask(width, height)
    img_rgba = img.convert("RGBA")
    output.paste(img_rgba, (0, 0), mask)

    # Drop shadow under avatar if requested
    bezel = config.get("bezel", 0)
    if config.get("drop_shadow") and bezel > 0:
        blurred = mask.filter(ImageFilter.GaussianBlur(radius=bezel * 2))
        shadow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        shadow_layer.putalpha(blurred)
        output = Image.alpha_composite(shadow_layer, output)

    # Bezel mask (apply full mask alpha)
    output.putalpha(mask)

    # Resize according to retina scale
    retina = config.get("retina_scale", 1)
    target_w = int(width * retina)
    target_h = int(height * retina)
    if target_w > 0 and target_h > 0:
        output = output.resize((target_w, target_h), Image.LANCZOS)

    # Grayscale if requested
    if config.get("grayscale"):
        output = output.convert("L").convert("RGBA")

    return output
