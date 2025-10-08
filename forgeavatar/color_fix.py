# ────────────────────────────────────────────────────────────────────────────
# color_fix.py
#
# • Lightweight colour revival helpers
# • Steps: automatic white-balance  → LAB-space CLAHE
# • Public API: `revive_colour(img)`
# ────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import logging

import cv2
import numpy as np
from PIL import Image

from forgeavatar.utils import configure_logging

logger = configure_logging(__name__)

__all__: list[str] = [
    "auto_white_balance",
    "clahe_lab",
    "revive_colour",
]


# ────────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────────
def _pil_to_bgr(img: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR)


def _bgr_to_pil(arr: np.ndarray) -> Image.Image:
    rgb = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb).convert("RGBA")


# ────────────────────────────────────────────────────────────────────────────
# Public algorithms
# ────────────────────────────────────────────────────────────────────────────
def auto_white_balance(img: Image.Image) -> Image.Image:
    """Simple gray-world WB."""
    bgr = _pil_to_bgr(img).astype(np.float32)
    avg = bgr.reshape(-1, 3).mean(axis=0)
    scale = avg.mean() / (avg + 1e-6)
    wb = np.clip(bgr * scale, 0, 255).astype(np.uint8)
    return _bgr_to_pil(wb)


def clahe_lab(img: Image.Image) -> Image.Image:
    """Apply CLAHE to L* channel in CIELab colour-space."""
    bgr = _pil_to_bgr(img)
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)
    merged = cv2.merge([l_eq, a, b])
    out = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    return _bgr_to_pil(out)


def revive_colour(img: Image.Image) -> Image.Image:
    """Run WB + CLAHE in sequence."""
    logger.debug("Running colour revival")
    return clahe_lab(auto_white_balance(img))
