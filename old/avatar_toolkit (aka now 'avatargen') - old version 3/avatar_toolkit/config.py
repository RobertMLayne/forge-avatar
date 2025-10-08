from __future__ import annotations

"""
avatar_toolkit/config.py - Configuration defaults and constants.

Responsibilities:
- Provide default values for avatar generation
- Export configuration dictionary
"""

__version__ = "1.0.0"
__all__ = ["DEFAULTS"]

DEFAULTS: dict[str, object] = {
    "width": 1584,
    "height": 396,
    "dpi": 96,
    "bezel": 4,
    "oversample": 16,
    "bg_color": None,
    "corner_radius": 0,
    "grayscale": False,
    "drop_shadow": True,
    "retina_scale": 3,
    "format": "PNG",
    "quality": 95,
    "lossless": False,
    "output_dir": "output",
    "face_detect": False,
    "auto_crop": False,
}
