# ────────────────────────────────────────────────────────────────────────────
# cli.py
#
# • Rich command-line interface for ForgeAvatar
# • Exposes all quality-boost flags added in v1.1
# ────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Final

from PIL import Image

from forgeavatar import __version__
from forgeavatar.config import DEFAULT_CONFIG
from forgeavatar.core import run_single
from forgeavatar.gui import launch_gui
from forgeavatar.utils import configure_logging, slugify

logger = configure_logging(__name__)

__all__: list[str] = ["build_parser", "main"]

# ────────────────────────────────────────────────────────────────────────────
# CLI helper
# ────────────────────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    """Return an `ArgumentParser` pre-configured with all flags."""
    p = argparse.ArgumentParser(
        prog="avatargen",
        description="ForgeAvatar – remaster low-res images to polished avatars",
    )
    p.add_argument("-i", "--input", required=False, help="Input image path")
    p.add_argument("-o", "--output", help="Output file (auto if omitted)")
    p.add_argument(
        "-f",
        "--format",
        default=DEFAULT_CONFIG["format"],
        choices=["PNG", "JPEG", "WEBP"],
        help="Output format",
    )

    # Quality group
    q = p.add_argument_group("quality")
    q.add_argument("--sr-scale", type=int, default=2, help="Super-res scale")
    q.add_argument(
        "--sr-backend",
        choices=["auto", "realesrgan", "opencv"],
        default="auto",
        help="Super-res engine",
    )
    q.add_argument("--no-face-restore", action="store_true", help="Skip GFPGAN")
    q.add_argument("--no-color-fix", action="store_true", help="Skip WB+CLAHE")
    q.add_argument("--lossless", action="store_true", help="WEBP lossless")
    q.add_argument("--quality", type=int, default=95, help="JPEG/WebP quality")

    # Style group
    s = p.add_argument_group("style")
    s.add_argument("--bezel", type=int, default=4, help="Bezel width px")
    s.add_argument("--corner-radius", type=int, default=16, help="Radius px")
    s.add_argument("--no-shadow", action="store_true", help="Disable shadow")

    # Misc
    p.add_argument("--gui", action="store_true", help="Launch drag-and-drop GUI")
    p.add_argument("-V", "--version", action="version", version=f"ForgeAvatar {__version__}")
    return p


def _build_config(ns: argparse.Namespace) -> dict:
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(
        {
            "sr_scale": ns.sr_scale,
            "sr_backend": ns.sr_backend,
            "face_restore": not ns.no_face_restore,
            "color_fix": not ns.no_color_fix,
            "bezel": ns.bezel,
            "corner_radius": ns.corner_radius,
            "drop_shadow": not ns.no_shadow,
            "lossless": ns.lossless,
            "quality": ns.quality,
            "format": ns.format,
        }
    )
    return cfg


# ────────────────────────────────────────────────────────────────────────────
# Entrypoint
# ────────────────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> None:  # noqa: D401
    """CLI entry-point (optionally pass *argv* for testing)."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.gui:
        launch_gui()
        return

    if not args.input:
        parser.error("`--input` required (or use --gui)")

    in_path = Path(args.input)
    if not in_path.exists():
        parser.error(f"File not found: {in_path}")

    out_path = Path(
        args.output or slugify(in_path.stem) + f".{args.format.lower()}"
    )

    cfg = _build_config(args)
    try:
        img = Image.open(in_path).convert("RGBA")
        run_single(img, str(out_path), cfg)
    except Exception as exc:  # pragma: no cover
        logger.error("Processing failed: %s", exc)
        sys.exit(1)

    logger.info("Avatar written → %s", out_path)


if __name__ == "__main__":  # pragma: no cover
    main()
