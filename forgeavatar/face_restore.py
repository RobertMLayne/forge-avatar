# ────────────────────────────────────────────────────────────────────────────
# face_restore.py
#
# • Optional face-clean-up stage using GFPGAN 1.x
# • Falls back to a no-op if the wheel (or a CUDA GPU) is unavailable
# • Public helper: `restore_face(img)` – returns a Pillow Image
# ────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import logging
from pathlib import Path
from typing import Final

import numpy as np
from PIL import Image

from forgeavatar.utils import configure_logging

logger = configure_logging(__name__)

__all__: list[str] = ["FaceRestorer", "restore_face"]

_CHECK_SIZE: Final[int] = 64  # px² minimum to attempt restoration


# ────────────────────────────────────────────────────────────────────────────
# Implementation
# ────────────────────────────────────────────────────────────────────────────
class _GFPGANWrapper:
    """Thin wrapper that hides heavy GFPGAN internals from callers."""

    def __init__(self) -> None:
        try:
            from gfpgan import GFPGANer  # noqa: WPS433
        except ModuleNotFoundError as exc:
            raise ImportError("GFPGAN not installed") from exc

        model_root = Path.home() / ".cache" / "forgeavatar"
        model_root.mkdir(parents=True, exist_ok=True)

        self._engine = GFPGANer(
            model_path="GFPGANv1.4.pth",
            upscale=1,
            arch="clean",
            channel_multiplier=2,
            bg_upsampler=None,
            model_scale=2,
            device="cuda" if self._has_cuda() else "cpu",
            model_root=str(model_root),
        )
        logger.info("GFPGAN initialised on %s", self._engine.device)

    # ------------------------------------------------------------------
    @staticmethod
    def _has_cuda() -> bool:  # pragma: no cover (hardware-specific)
        try:
            import torch  # noqa: WPS433

            return torch.cuda.is_available()
        except ModuleNotFoundError:
            return False

    # ------------------------------------------------------------------
    def restore(self, img: Image.Image) -> Image.Image:
        """Run face enhancement and return a new RGBA Pillow image."""
        rgb = img.convert("RGB")
        np_img = np.array(rgb)
        _, _, restored = self._engine.enhance(np_img, has_aligned=False)
        return Image.fromarray(restored).convert("RGBA")


# ────────────────────────────────────────────────────────────────────────────
# Public façade
# ────────────────────────────────────────────────────────────────────────────
class FaceRestorer:
    """Facade that delegates to GFPGAN or noop."""

    def __init__(self) -> None:
        try:
            self._backend: _GFPGANWrapper | None = _GFPGANWrapper()
        except ImportError:
            self._backend = None
            logger.info("GFPGAN unavailable → face-restore disabled")

    # ------------------------------------------------------------------
    def restore(self, img: Image.Image) -> Image.Image:
        """Return restored image (or original if backend missing)."""
        if (
            self._backend is None
            or min(img.size) < _CHECK_SIZE  # too small to justify
        ):
            return img
        try:
            return self._backend.restore(img)
        except Exception as exc:  # pragma: no cover
            logger.warning("GFPGAN failed (%s) – returning original", exc)
            return img


# Singleton used by helper
_restorer: FaceRestorer | None = None


def restore_face(img: Image.Image) -> Image.Image:
    """Module-level convenience wrapper."""
    global _restorer
    if _restorer is None:
        _restorer = FaceRestorer()
    return _restorer.restore(img)
