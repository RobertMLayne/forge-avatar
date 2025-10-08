# ────────────────────────────────────────────────────────────────────────────
# processing.py
#
# • Master image-processing pipeline for ForgeAvatar
# • Chains super-resolution → face restore → colour revival →
#   framing / bezel / mask → drop-shadow
# • Designed to be import-side-effect free; all heavy libs are
#   loaded lazily in sub-modules
# ────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import logging
from typing import Final

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from forgeavatar.color_fix import revive_colour
from forgeavatar.face_restore import restore_face
from forgeavatar.superres import upscale_image
from forgeavatar.utils import configure_logging

logger = configure_logging(__name__)

__all__: list[str] = ["process_image"]

# ────────────────────────────────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────────────────────────────────
TARGET_W: Final[int] = 1_584
TARGET_H: Final[int] = 396
RGBA_TRANSPARENT: Final[tuple[int, int, int, int]] = (0, 0, 0, 0)


# ────────────────────────────────────────────────────────────────────────────
# Public orchestrator
# ────────────────────────────────────────────────────────────────────────────
def process_image(img: Image.Image, config: dict) -> Image.Image:
    """
    Run the full ForgeAvatar pipeline on *img* using *config*.

    Returns a brand-new Pillow RGBA image 1584 × 396 px.
    """
    logger.info("⟳ ForgeAvatar pipeline start")
    work = img.convert("RGBA")

    # 1. Super-resolution
    scale = int(config.get("sr_scale", 2))
    if scale > 1:
        work = upscale_image(work, scale)
        logger.debug("SR done (%sx)", scale)

    # 2. Face restoration
    if config.get("face_restore", True):
        work = restore_face(work)
        logger.debug("Face restore done")

    # 3. Colour revival
    if config.get("color_fix", True):
        work = revive_colour(work)
        logger.debug("Colour revival done")

    # 4. Frame / pad into target aspect (blurred edges)
    work = _pad_to_banner(work)
    logger.debug("Framing done")

    # 5. Rounded mask
    corner = int(config.get("corner_radius", 16))
    work = _apply_round_mask(work, corner)
    logger.debug("Mask done")

    # 6. Tri-tone bezel
    bezel = int(config.get("bezel", 4))
    if bezel:
        work = _apply_bezel(work, bezel)
        logger.debug("Bezel drawn")

    # 7. Drop-shadow
    if config.get("drop_shadow", True):
        work = _drop_shadow(work)
        logger.debug("Shadow applied")

    logger.info("✓ ForgeAvatar pipeline complete")
    return work


# ────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ────────────────────────────────────────────────────────────────────────────
def _pad_to_banner(src: Image.Image) -> Image.Image:
    """
    Return *src* centred on a 1584 × 396 canvas.

    Adds blurred edge padding if aspect ratios clash.
    """
    canvas = Image.new("RGBA", (TARGET_W, TARGET_H), RGBA_TRANSPARENT)
    sw, sh = src.size
    scale = min(TARGET_W / sw, TARGET_H / sh)
    new_size = (int(sw * scale), int(sh * scale))
    resized = src.resize(new_size, Image.Resampling.LANCZOS)

    # Centre
    off_x = (TARGET_W - new_size[0]) // 2
    off_y = (TARGET_H - new_size[1]) // 2
    canvas.paste(resized, (off_x, off_y))

    # Fast blurred-edge fill
    if off_x or off_y:
        blur = resized.filter(ImageFilter.GaussianBlur(12))
        if off_x:
            canvas.paste(
                blur.resize((off_x, TARGET_H)),
                (0, 0),
            )
            canvas.paste(
                blur.resize((off_x, TARGET_H)),
                (TARGET_W - off_x, 0),
            )
        if off_y:
            canvas.paste(
                blur.resize((TARGET_W, off_y)),
                (0, 0),
            )
            canvas.paste(
                blur.resize((TARGET_W, off_y)),
                (0, TARGET_H - off_y),
            )

    return canvas


def _apply_round_mask(img: Image.Image, radius: int) -> Image.Image:
    """Clip *img* with a rounded-rectangle alpha mask."""
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        [(0, 0), img.size],
        radius=radius,
        fill=255,
    )
    out = img.copy()
    out.putalpha(mask)
    return out


def _apply_bezel(img: Image.Image, width: int) -> Image.Image:
    """Draw gold-black-gold tri-tone bezel around *img*."""
    w, h = img.size
    bezel_img = Image.new("RGBA", img.size, RGBA_TRANSPARENT)
    draw = ImageDraw.Draw(bezel_img)

    def _ellipse(offset: int, colour: tuple[int, int, int]) -> None:
        draw.rounded_rectangle(
            [(offset, offset), (w - offset, h - offset)],
            radius=16,
            outline=colour,
            width=1,
        )

    gold = (212, 175, 55)
    black = (0, 0, 0)
    for i in range(width):
        col = gold if i in (0, width - 1) else black
        _ellipse(i, (*col, 255))
    return Image.alpha_composite(img, bezel_img)


def _drop_shadow(img: Image.Image) -> Image.Image:
    """Cheap drop-shadow: 2 px offset, α64 Gaussian 4."""
    base = Image.new("RGBA", (img.width + 4, img.height + 4), RGBA_TRANSPARENT)
    shadow = img.split()[3].filter(ImageFilter.GaussianBlur(4))
    shadow_img = Image.new("RGBA", base.size, (0, 0, 0, 64))
    base.paste(shadow_img, (4, 4), shadow)
    base.paste(img, (0, 0), img)
    return base.crop((0, 0, img.width, img.height))
