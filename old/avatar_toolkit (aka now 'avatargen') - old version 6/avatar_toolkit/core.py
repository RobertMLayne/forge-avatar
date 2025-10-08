from __future__ import annotations

"""
avatar_toolkit/core.py - Core image processing logic for avatar generation.

Responsibilities:
• Process a single image with given configuration
• Save or return the processed image
"""
__version__ = "1.0.0"
__all__ = ["run_single"]

import logging
import os
from pathlib import Path
from typing import Any, Optional, Union

from PIL import Image

from .config import DEFAULTS
from .processing import process_image
from .utils import ensure_dir, configure_logging

logger = logging.getLogger(__name__)

def run_single(
    img: Union[str, Image.Image],
    output_path: Optional[Union[str, Path]],
    config: dict[str, Any],
    return_image: bool = False
) -> Optional[Image.Image]:
    """Process an image and optionally save or return it."""
    configure_logging()
    # Support legacy 'output_format' key
    if "output_format" in config:
        config["format"] = config.pop("output_format")

    # Load image if file path given
    if isinstance(img, (str, Path)):
        image = Image.open(img).convert("RGBA")
    else:
        image = img

    # Process image
    result = process_image(image, config)

    # Save result if output path provided
    if output_path:
        out_dir = os.path.dirname(str(output_path)) or "."
        ensure_dir(out_dir)
        save_kwargs: dict[str, Any] = {}
        fmt = config.get("format", DEFAULTS["format"])
        save_kwargs["format"] = fmt
        if fmt.upper() in ("JPEG", "WEBP"):
            save_kwargs["quality"] = config.get("quality", DEFAULTS["quality"])
            if fmt.upper() == "WEBP":
                save_kwargs["lossless"] = config.get(
                    "lossless", DEFAULTS["lossless"]
                )
        result.save(output_path, **save_kwargs)
        logger.info("Saved image: %s", output_path)

    if return_image:
        return result
    return None
