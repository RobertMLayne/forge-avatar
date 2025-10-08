from __future__ import annotations

"""
avatar_toolkit/core.py - Core image processing logic for avatar generation.

Responsibilities:
- Process a single image with given configuration
- Save or return the processed image
"""

__version__ = "1.0.0"
__all__ = ["run_single"]

import os
from pathlib import Path
from typing import Optional, Union

from PIL import Image

from .processing import process_image
from .utils import ensure_dir


def run_single(
    img: Union[Image.Image, str],
    output_path: Optional[str | Path],
    config: dict[str, object],
    return_image: bool = False
) -> Optional[Image.Image]:
    """Process an image and optionally save or return it."""
    # Configure logging if needed
    from .utils import configure_logging

    configure_logging()

    # Open image if path is provided
    if isinstance(img, (str, Path)):
        img = Image.open(img).convert("RGBA")  # type: ignore

    # Process image
    result = process_image(img, config)

    # Save result if output path provided
    if output_path:
        out_path = Path(output_path)
        # Ensure output directory exists
        ensure_dir(out_path.parent)
        save_kwargs: dict[str, object] = {
            "format": config.get("format", None) or config.get("output_format", None),
            "optimize": True,
        }
        fmt = save_kwargs.get("format")
        if fmt:
            fmt = fmt.upper()
            save_kwargs["format"] = fmt
            if fmt in ["JPEG", "WEBP"]:
                save_kwargs["quality"] = config.get("quality", 95)
            if fmt == "WEBP":
                save_kwargs["lossless"] = config.get("lossless", False)
        result.save(out_path, **{k: v for k, v in save_kwargs.items() if v is not None})

    if return_image:
        return result
    return None
