from __future__ import annotations

"""avatar_toolkit/cli.py - Command-line interface for avatar processing.

Responsibilities:
• Parse command-line arguments
• Invoke processing for a single image
"""
__version__ = "1.0.0"
__all__ = ["main"]

import argparse
from pathlib import Path
import logging

from PIL import Image

from .core import run_single
from .config import DEFAULTS
from .utils import configure_logging

logger = logging.getLogger(__name__)

def main() -> None:
    """Main CLI entry point."""
    configure_logging()
    parser = argparse.ArgumentParser(description="Avatar Generator CLI")
    parser.add_argument(
        "--input", type=Path, required=True,
        help="Input image file"
    )
    parser.add_argument(
        "--output", type=Path, required=True,
        help="Output file path"
    )
    parser.add_argument(
        "--format",
        choices=["PNG", "JPEG", "WEBP"],
        default=DEFAULTS["format"],
        help="Output image format"
    )
    parser.add_argument(
        "--quality", type=int,
        default=DEFAULTS["quality"],
        help="Quality for JPEG/WebP"
    )
    parser.add_argument(
        "--lossless", action="store_true",
        help="Use lossless WebP encoding"
    )
    parser.add_argument(
        "--grayscale", action="store_true",
        help="Convert image to grayscale"
    )
    parser.add_argument(
        "--drop-shadow", action="store_true",
        help="Apply drop shadow to avatar"
    )
    parser.add_argument(
        "--face-detect", action="store_true",
        help="Enable face detection and auto-crop"
    )
    args = parser.parse_args()
    img = Image.open(args.input).convert("RGBA")
    config = DEFAULTS.copy()
    config.update(vars(args))
    run_single(img, args.output, config)
