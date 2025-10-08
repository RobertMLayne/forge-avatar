from __future__ import annotations

"""avatar_toolkit/__init__.py - Main package interface.

Responsibilities:
• Expose main functions of the avatar toolkit
• Provide package version and exports
"""

__version__ = "1.0.0"
__all__ = [
    "run_single",
    "DEFAULTS",
    "launch_gui",
    "cli_main",
    "run_batch",
    "process_image",
]

from .core import run_single
from .config import DEFAULTS
from .gui import launch_gui
from .cli import main as cli_main
from .batch import run_batch
from .processing import process_image
