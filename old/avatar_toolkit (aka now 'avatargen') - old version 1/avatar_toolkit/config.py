# config.py
"""Configuration defaults and constants."""

DEFAULTS = {
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
    "auto_crop": False
}

__all__ = ["DEFAULTS"]
