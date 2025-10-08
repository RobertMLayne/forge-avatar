# cli.py
"""Command-line interface for avatar processing."""

import argparse
from PIL import Image
from .core import run_single
from .config import DEFAULTS


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Avatar Generator CLI")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--format", choices=["PNG", "JPEG", "WEBP"], default=DEFAULTS["format"])
    parser.add_argument("--quality", type=int, default=DEFAULTS["quality"])
    parser.add_argument("--lossless", action="store_true")
    parser.add_argument("--grayscale", action="store_true")
    parser.add_argument("--drop-shadow", action="store_true")
    parser.add_argument("--face-detect", action="store_true")

    args = parser.parse_args()
    img = Image.open(args.input).convert("RGBA")

    config = DEFAULTS.copy()
    config.update(vars(args))

    run_single(img, args.output, config)

__all__ = ["main"]
