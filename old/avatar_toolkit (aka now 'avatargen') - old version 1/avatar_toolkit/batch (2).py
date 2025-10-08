# batch.py
"""Batch processing of avatar generation for all images in a directory."""

import os
from PIL import Image
from .core import run_single


def run_batch(input_dir, output_dir, config):
    """Process all images in a directory with given config."""
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            in_path = os.path.join(input_dir, filename)
            out_name = os.path.splitext(filename)[0] + f"_processed.{config['format'].lower()}"
            out_path = os.path.join(output_dir, out_name)
            img = Image.open(in_path).convert("RGBA")
            run_single(img, out_path, config)

__all__ = ["run_batch"]
