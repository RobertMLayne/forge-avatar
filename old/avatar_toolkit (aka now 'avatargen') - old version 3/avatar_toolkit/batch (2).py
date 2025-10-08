from __future__ import annotations

"""
avatar_toolkit/batch.py - Batch processing of avatar generation for all images in a directory.

Responsibilities:
- Process all image files in a directory using given configuration
"""

__version__ = "1.0.0"
__all__ = ["run_batch"]

import os
from pathlib import Path
from typing import Any

from PIL import Image

from .core import run_single


def run_batch(
    input_dir: str | Path, output_dir: str | Path, config: dict[str, Any]
) -> None:
    """Process all images in a directory with given config."""
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            in_path = os.path.join(input_dir, filename)
            out_name = Path(filename).stem + f"_processed.{config['format'].lower()}"
            out_path = os.path.join(output_dir, out_name)
            img = Image.open(in_path).convert("RGBA")
            run_single(img, out_path, config)
