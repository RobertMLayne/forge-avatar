# ──────────────────────────────────────────────────────────────────────────
# superres.py
#
# • Pluggable super-resolution back-end for ForgeAvatar
# • Prefers Real-ESRGAN (GPU/CPU) → falls back to OpenCV-DNN EDSR → Pillow
# • All methods pure-Python; no torch objects leak to callers
# ──────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import hashlib
import logging
import sys
from pathlib import Path
from typing import Final, Protocol

import numpy as np
from PIL import Image

from forgeavatar.utils import configure_logging, cache_dir

logger = configure_logging(__name__)

__all__: list[str] = [
    "SuperResolutionError",
    "SuperResolutionBackend",
    "RealESRGANBackend",
    "OpenCVSRBackend",
    "AutoSRBackend",
]

# ──────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────
_DEFAULT_SCALE: Final[int] = 2
_MAX_SCALE: Final[int] = 4

# ──────────────────────────────────────────────────────────────────────────
# Exceptions
# ──────────────────────────────────────────────────────────────────────────
class SuperResolutionError(RuntimeError):
    """Raised when SR upscaling fails irrecoverably."""


# ──────────────────────────────────────────────────────────────────────────
# Protocol / base interface
# ──────────────────────────────────────────────────────────────────────────
class SuperResolutionBackend(Protocol):
    """Interface for all SR engines."""

    name: str

    def upscale(self, img: Image.Image, scale: int = _DEFAULT_SCALE) -> Image.Image:  # noqa: D401
        """Return a new Pillow image up-scaled by *scale*."""
        ...


# ──────────────────────────────────────────────────────────────────────────
# Real-ESRGAN back-end (optional)
# ──────────────────────────────────────────────────────────────────────────
class RealESRGANBackend:
    """Wrapper around `realesrgan` package (GPU→CPU fallback)."""

    name = "realesrgan"

    _model_cls: Final[str] = "realesrgan.RealESRGAN"

    def __init__(self) -> None:
        try:
            import realesrgan  # noqa: WPS433 (dynamic import)
            import torch  # noqa: WPS433
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise ImportError("realesrgan not installed") from exc

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = realesrgan.RealESRGAN(device, scale=2)
        self._model.load_weights("RealESRGAN_x2.pth")

        # Pre-load 4× weights lazily
        self._model4 = None
        logger.info("Real-ESRGAN initialised on %s", device)

    # ----------------------------------------------------------
    def upscale(self, img: Image.Image, scale: int = _DEFAULT_SCALE) -> Image.Image:
        if scale not in (2, 4):
            raise ValueError("Real-ESRGAN supports only 2× or 4× scale")

        if scale == 4 and self._model4 is None:
            # Lazy-load 4× weights
            from realesrgan import RealESRGAN  # local import to keep header clean

            self._model4 = RealESRGAN(self._model.device, scale=4)
            self._model4.load_weights("RealESRGAN_x4.pth")

        model = self._model if scale == 2 else self._model4
        assert model is not None
        logger.debug("Upscaling via Real-ESRGAN %sx", scale)
        return model.predict(img)


# ──────────────────────────────────────────────────────────────────────────
# OpenCV back-end (always available via opencv-python-headless)
# ──────────────────────────────────────────────────────────────────────────
class OpenCVSRBackend:
    """Fallback SR using OpenCV’s EDSR model (CPU-only, slower)."""

    name = "opencv-edsr"

    def __init__(self) -> None:
        import cv2  # noqa: WPS433

        self._cv2 = cv2
        self._sr = cv2.dnn_superres.DnnSuperResImpl_create()
        model_path = self._download_model("EDSR_x2.pb")
        self._sr.readModel(str(model_path))
        self._sr.setModel("edsr", 2)
        logger.info("OpenCV EDSR model loaded")

    # ----------------------------------------------------------
    def upscale(self, img: Image.Image, scale: int = _DEFAULT_SCALE) -> Image.Image:
        if scale not in (2, 4):
            raise ValueError("OpenCV EDSR supports only 2× or 4×")

        if scale == 4:
            model_path = self._download_model("EDSR_x4.pb")
            self._sr.readModel(str(model_path))
            self._sr.setModel("edsr", 4)

        arr = self._cv2.cvtColor(np.array(img), self._cv2.COLOR_RGBA2RGB)
        out = self._sr.upsample(arr)
        out_rgba = self._cv2.cvtColor(out, self._cv2.COLOR_RGB2RGBA)
        return Image.fromarray(out_rgba)

    # ----------------------------------------------------------
    def _download_model(self, filename: str) -> Path:
        """Fetch pre-trained model to cache dir if absent."""
        dst = cache_dir() / "opencv_models" / filename
        if dst.exists():
            return dst

        dst.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://github.com/Saafke/EDSR_Tensorflow/releases/download/2.0/{filename}"  # noqa: E501
        logger.info("Downloading %s …", filename)
        import urllib.request as _url  # noqa: WPS433

        with _url.urlopen(url) as resp, open(dst, "wb") as fh:  # noqa: S310
            fh.write(resp.read())
        return dst


# ───────────────────────────────────────────────────────────────
# Auto-selector
# ───────────────────────────────────────────────────────────────
class AutoSRBackend:
    """Choose the fastest available SR engine."""

    def __init__(self) -> None:
        self._backend: SuperResolutionBackend
        try:
            self._backend = RealESRGANBackend()
        except ImportError:
            logger.info("Real-ESRGAN unavailable → using OpenCV EDSR")
            self._backend = OpenCVSRBackend()

    # ----------------------------------------------------------
    @property
    def name(self) -> str:  # noqa: D401
        """Human-readable back-end name."""
        return self._backend.name

    # ----------------------------------------------------------
    def upscale(self, img: Image.Image, scale: int = _DEFAULT_SCALE) -> Image.Image:
        scale = min(max(2, scale), _MAX_SCALE)
        cache_key = self._cache_key(img, scale)
        cached = cache_dir() / "sr" / f"{cache_key}.png"
        if cached.exists():
            logger.debug("SR cache hit %s", cached.name)
            return Image.open(cached)

        out = self._backend.upscale(img, scale)
        cached.parent.mkdir(parents=True, exist_ok=True)
        out.save(cached, format="PNG")
        return out

    # ----------------------------------------------------------
    @staticmethod
    def _cache_key(img: Image.Image, scale: int) -> str:
        h = hashlib.sha1()
        h.update(img.tobytes())
        h.update(str(scale).encode())
        return h.hexdigest()[:16]


# ───────────────────────────────────────────────────────────────
# Convenience singleton
# ───────────────────────────────────────────────────────────────
_sr_singleton: AutoSRBackend | None = None


def upscale_image(img: Image.Image, scale: int = _DEFAULT_SCALE) -> Image.Image:
    """Public helper for callers that just need an upscaled image."""
    global _sr_singleton
    if _sr_singleton is None:
        _sr_singleton = AutoSRBackend()
        logger.info("SR backend chosen: %s", _sr_singleton.name)
    return _sr_singleton.upscale(img, scale)
