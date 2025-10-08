# avatar_toolkit/config.py
"""Default configuration values and constants for Avatar Toolkit."""
import cv2

# Default path to Haar Cascade model for face detection (OpenCV)
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Default avatar output size (pixels)
AVATAR_SIZE = 256

# Allowed image file extensions for processing (if needed in future)
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}

DEFAULTS: dict = {
    "width": 1584,       # Output image width (e.g. 11 inches at 144 dpi)
    "height": 396,       # Output image height
    "dpi": 144,          # DPI for high-res output (96 is standard; 144 for retina)
    "bezel": 4,          # Bezel thickness in pixels
    "oversample": 16,
    "bg_color": None,    # Background color (None for transparent)
    "corner_radius": 16, # Rounded corner radius for avatar mask
    "grayscale": False,
    "drop_shadow": True,
    "retina_scale": 3,
    "format": "PNG",     # Default output format
    "quality": 100,       # Quality for lossy formats like JPEG/WebP
    "lossless": True,
    "output_dir": "C:\Dev\projects\avatar_toolkit - revised\output",
    "face_detect": True,
    "auto_crop": False
}

# High-DPI (Retina) display scaling for GUI (Windows-specific)
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)   # Windows 8.1+ DPI awareness:contentReference[oaicite:1]{index=1}
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()    # Windows 8.0 and earlier:contentReference[oaicite:2]{index=2}
    except Exception:
        pass

# On macOS, Tk is DPI-aware by default. On Windows, one can also use:
# import tkinter; tkinter.Tk().tk.call('tk', 'scaling', scaling_factor)
# if explicit scaling is needed (usually handled by DPI awareness above).

__all__ = ["DEFAULTS"]
