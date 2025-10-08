from __future__ import annotations

"""
avatar_toolkit/batch.py - Batch processing for all images in a directory.

Responsibilities:
• Process all image files in a directory using given configuration
"""
__version__ = "1.0.0"
__all__ = ["run_batch"]

import logging
import os
from pathlib import Path
from typing import Any, Union

from PIL import Image

from .core import run_single

logger = logging.getLogger(__name__)

def run_batch(
    input_dir: Union[str, Path],
    output_dir: Union[str, Path],
    config: dict[str, Any]
) -> None:
    """Process all images in a directory with given config."""
    logger.info("Starting batch processing: %s -> %s", input_dir, output_dir)
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            logger.info("Processing %s", filename)
            in_path = os.path.join(input_dir, filename)
            base = Path(filename).stem
            out_name = base + f"_processed.{config['format'].lower()}"
            out_path = os.path.join(output_dir, out_name)
            img = Image.open(in_path).convert("RGBA")
            run_single(img, out_path, config)
