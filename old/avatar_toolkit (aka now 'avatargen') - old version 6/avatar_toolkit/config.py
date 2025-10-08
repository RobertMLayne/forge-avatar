from __future__ import annotations

"""
avatar_toolkit/config.py - Configuration defaults and constants.

Responsibilities:
• Provide default values for avatar generation
• Store constants such as default DPI, resize values, and model paths
"""
__version__ = "1.0.0"
__all__ = ["DEFAULTS"]

import cv2

# High-DPI (Retina) display scaling for GUI (Windows-specific)
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Windows 8.1+
    try:
        ctypes.windll.user32.SetProcessDPIAware()     # Windows 8.0+
    except Exception:
        pass
except ImportError:
    pass

DEFAULTS: dict[str, object] = {
    # Output image size and DPI
    "width": 1584,        # Output image width in pixels
    "height": 396,        # Output image height in pixels
    "dpi": 144,           # DPI for output (144 for high-res)
    # Visual styling
    "bezel": 4,           # Bezel thickness in pixels
    "oversample": 16,     # Supersample factor for smoothing (reserved)
    "bg_color": None,     # Background color (None for transparent)
    "corner_radius": 16,  # Rounded corner radius for mask
    "grayscale": False,
    "drop_shadow": True,
    "retina_scale": 3,    # Scaling factor for retina displays
    "format": "PNG",
    "quality": 95,
    "lossless": True,     # Use lossless WebP by default
    "output_dir": "output",
    "face_detect": True,   # Perform face detection and auto-crop by default
    "auto_crop": False,    # Crop to content bounding box by default
}
