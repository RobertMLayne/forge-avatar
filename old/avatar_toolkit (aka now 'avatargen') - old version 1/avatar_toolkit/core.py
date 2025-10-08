# core.py
"""Core image processing logic for avatar generation."""

import os
from PIL import Image
from .processing import process_image
from .config import DEFAULTS

def run_single(img: Image.Image, output_path: str, config: dict) -> None:
    """Process and save a single image using the provided configuration."""
    result = process_image(img, config)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    save_kwargs = {
        "format": config.get("format", DEFAULTS["format"]),
        "optimize": True
    }

    if save_kwargs["format"].upper() in ["JPEG", "WEBP"]:
        save_kwargs["quality"] = config.get("quality", 95)
        if save_kwargs["format"].upper() == "WEBP":
            save_kwargs["lossless"] = config.get("lossless", False)

    result.save(output_path, **save_kwargs)

__all__ = ["run_single"]
