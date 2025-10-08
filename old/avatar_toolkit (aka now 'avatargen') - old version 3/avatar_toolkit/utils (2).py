from __future__ import annotations

"""
avatar_toolkit/utils.py - Utility functions for file and logging.

Responsibilities:
- File and path utilities (slugify, ensure directories, etc.)
- Logging configuration
"""

__version__ = "1.0.0"
__all__ = [
    "slugify",
    "ensure_dir",
    "infer_output_filename",
    "is_image_file",
    "configure_logging",
]

import os
import re
import logging
from pathlib import Path
from typing import Optional


def configure_logging(level: int = logging.INFO) -> None:
    """Configure basic logging with a default format and level."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def slugify(text: str) -> str:
    """Converts text to a filesystem-safe slug."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text).strip('_').lower()


def ensure_dir(path: str | Path) -> None:
    """Creates the directory if it does not exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


def infer_output_filename(
    input_path: str | Path, suffix: str = "_out", ext: Optional[str] = None
) -> str:
    """Generates an output filename by appending a suffix to the stem."""
    p = Path(input_path)
    new_ext = ext if ext else p.suffix
    return str(p.with_name(p.stem + suffix).with_suffix(new_ext))


def is_image_file(path: str | Path) -> bool:
    """Checks if the file has a known image extension."""
    return Path(path).suffix.lower() in {
        ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"
    }
