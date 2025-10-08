"""
Image processing module.
"""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

from PIL import Image

import logging

logger = logging.getLogger(__name__)

__all__ = ["ImageProcessor"]

class ImageProcessor:
    """
    Processes images to create avatar outputs.
    Supports cropping faces and saving with specified formats.
    """
    def __init__(self, output_format: str = "PNG",
                 jpeg_quality: int = 85, png_compression_level: int = 6) -> None:
        """
        Initialize the image processor.

        Args:
            output_format: "PNG" or "JPEG".
            jpeg_quality: Quality for JPEG format (1-100).
            png_compression_level: Compression level for PNG (0-9).
        """
        self.output_format = output_format.upper()
        self.jpeg_quality = jpeg_quality
        self.png_compression_level = png_compression_level
        if self.output_format not in ("PNG", "JPEG", "JPG"):
            logger.warning("Unsupported format %s, defaulting to PNG", self.output_format)
            self.output_format = "PNG"

    def crop_face(self, image: Image.Image, bbox: Tuple[int, int, int, int]) -> Image.Image:
        """
        Crop the image to the given bounding box.

        Args:
            image: PIL Image to crop.
            bbox: (x, y, w, h) bounding box.

        Returns:
            Cropped PIL Image.
        """
        x, y, w, h = bbox
        # Ensure coordinates are within image
        width, height = image.size
        x = max(0, x)
        y = max(0, y)
        w = min(w, width - x)
        h = min(h, height - y)
        cropped = image.crop((x, y, x + w, y + h))
        logger.debug("Cropped face region: %s", (x, y, w, h))
        return cropped

    def save(self, image: Image.Image, output_path: Path) -> None:
        """
        Save the image to a file with the configured format and quality/compression.

        Args:
            image: PIL Image to save.
            output_path: Path where the image will be saved.
        """
        fmt = self.output_format
        save_kwargs = {}
        if fmt in ("JPEG", "JPG"):
            save_kwargs["format"] = "JPEG"
            save_kwargs["quality"] = self.jpeg_quality
            save_kwargs["optimize"] = True
        elif fmt == "PNG":
            save_kwargs["format"] = "PNG"
            save_kwargs["optimize"] = True
            save_kwargs["compress_level"] = self.png_compression_level

        try:
            image.save(output_path, **save_kwargs)
            logger.info("Saved image: %s", output_path)
        except Exception as e:
            logger.exception("Failed to save image %s: %s", output_path, e)
            raise
