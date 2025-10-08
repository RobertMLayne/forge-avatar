"""Command-line interface for Avatar Toolkit."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import List

from PIL import Image  # noqa: F401 (kept for future direct-open features)

from avatar_toolkit import __version__
from avatar_toolkit.batch import process_images
from avatar_toolkit.config import DEFAULT_CONFIG, load_config
from avatar_toolkit.core import AvatarGenerator
from avatar_toolkit.gui import main as launch_gui  # one-liner wrapper
from avatar_toolkit.utils import configure_logging, ensure_dir, is_image_file

__all__ = ["main"]


def _process_single(
    input_path: Path, output_dir: Path, generator: AvatarGenerator
) -> List[Path]:
    """Run face-detect → crop → save on one image and return output paths."""
    outputs = generator.process_image(input_path, output_dir)
    if outputs:
        logging.info("✔ %s → %d file(s)", input_path.name, len(outputs))
    else:
        logging.warning("No faces detected in %s", input_path)
    return outputs


def main() -> None:
    """Entry-point installed as the `avatargen` console script."""
    parser = argparse.ArgumentParser(
        prog="avatargen",
        description="Avatar Toolkit – generate polished avatars from images.",
    )
    parser.add_argument(
        "-i", "--input", required=False, help="Input file or directory path."
    )
    parser.add_argument(
        "-o", "--output", required=False, help="Directory where outputs are saved."
    )
    parser.add_argument(
        "-c", "--config", help="Optional YAML/JSON config overriding defaults."
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        help="Thread pool size when processing a directory (default from config).",
    )
    parser.add_argument(
        "--gui", action="store_true", help="Start the drag-and-drop GUI instead."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose (DEBUG) logging."
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"Avatar Toolkit {__version__}"
    )
    args = parser.parse_args()

    # ───── GUI mode ────────────────────────────────────────────────────────────
    if args.gui:
        launch_gui()
        return

    # ───── CLI mode validation ────────────────────────────────────────────────
    if not args.input or not args.output:
        parser.error("--input and --output are required unless you pass --gui.")

    log_level = logging.DEBUG if args.verbose else logging.INFO
    configure_logging(level=log_level)

    input_path = Path(args.input).expanduser()
    output_dir = ensure_dir(Path(args.output).expanduser())

    # ───── Load / merge configuration ─────────────────────────────────────────
    cfg = DEFAULT_CONFIG.copy()
    if args.config:
        try:
            cfg = load_config(args.config)
        except Exception as exc:  # pragma: no cover
            logging.error("Failed to load config: %s", exc)
            sys.exit(1)

    generator = AvatarGenerator(cfg)

    # ───── Directory (batch) vs. single file ─────────────────────────────────
    if input_path.is_dir():
        files = [
            str(p)
            for p in input_path.iterdir()
            if p.is_file() and is_image_file(p)
        ]
        if not files:
            logging.error("No image files found in %s", input_path)
            sys.exit(1)
        workers = args.workers or cfg.get("batch", {}).get("max_workers", 4)
        process_images(files, output_dir, config=cfg, max_workers=workers)
    else:
        if not is_image_file(input_path):
            logging.error("Unsupported image type: %s", input_path)
            sys.exit(1)
        _process_single(input_path, output_dir, generator)


if __name__ == "__main__":  # pragma: no cover
    main()
