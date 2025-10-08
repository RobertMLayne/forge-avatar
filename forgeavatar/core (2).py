# ────────────────────────────────────────────────────────────────────────────
# core.py
#
# • High-level entry-points that the CLI, GUI and batch modes call
# • Provides:
#     – `run_single(img, path, config)`  → one-off helper
#     – `AvatarGenerator` class for re-use across many images
# • Keeps all heavy lifting inside `processing.process_image`
# ────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, MutableMapping

from PIL import Image

from forgeavatar.config import DEFAULT_CONFIG
from forgeavatar.processing import process_image
from forgeavatar.utils import configure_logging

logger = configure_logging(__name__)

__all__: list[str] = ["run_single", "AvatarGenerator"]


# ────────────────────────────────────────────────────────────────────────────
# Functional helper
# ────────────────────────────────────────────────────────────────────────────
def run_single(
    img: Image.Image,
    output_path: str | Path,
    config: MutableMapping[str, Any] | None = None,
) -> None:
    """
    Process *img* according to *config* and write to *output_path*.

    *config* is merged on top of `DEFAULT_CONFIG`.  The output directory
    is created automatically.
    """
    cfg: Dict[str, Any] = {**DEFAULT_CONFIG, **(config or {})}
    logger.debug("run_single cfg=%s", cfg)

    result = process_image(img, cfg)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    save_kwargs: Dict[str, Any] = {"format": cfg["format"]}
    if cfg["format"] in {"JPEG", "WEBP"}:
        save_kwargs.update(
            quality=cfg["quality"],
            lossless=cfg.get("lossless", False),
        )

    result.save(out, **save_kwargs)
    logger.info("Image written → %s", out)


# ────────────────────────────────────────────────────────────────────────────
# OOP façade (useful for batch mode or GUI)
# ────────────────────────────────────────────────────────────────────────────
@dataclass(slots=True)
class AvatarGenerator:
    """
    Re-usable processor object.

    Parameters
    ----------
    base_config
        Dict merged into :pydata:`forgeavatar.config.DEFAULT_CONFIG`
        for every call.
    """

    base_config: Dict[str, Any]

    # ------------------------------------------------------------------
    def __post_init__(self) -> None:  # noqa: D401
        self.base_config = {**DEFAULT_CONFIG, **self.base_config}
        logger.debug("AvatarGenerator init cfg=%s", self.base_config)

    # ------------------------------------------------------------------
    def generate(
        self,
        img: Image.Image,
        *,
        output: str | Path | None = None,
        extra_cfg: MutableMapping[str, Any] | None = None,
    ) -> Image.Image:
        """
        Return a processed Pillow image; optionally save it to *output*.

        *extra_cfg* is layered over ``self.base_config`` just for this call.
        """
        cfg: Dict[str, Any] = {**self.base_config, **(extra_cfg or {})}
        result = process_image(img, cfg)

        if output:
            run_single(result, output, cfg)
        return result
