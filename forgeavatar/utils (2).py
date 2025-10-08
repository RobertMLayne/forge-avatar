# ────────────────────────────────────────────────────────────────────────────
# utils.py
#
# • Common helpers reused across ForgeAvatar
# • Unified logging configurator
# • X-platform cache directory helper
# • A few path/slug convenience functions needed by tests & CLI
# ────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path
from typing import Final, Optional

__all__: list[str] = [
    "configure_logging",
    "cache_dir",
    "slugify",
    "ensure_dir",
    "infer_output_filename",
]

# ────────────────────────────────────────────────────────────────────────────
# Logging
# ────────────────────────────────────────────────────────────────────────────
_FMT: Final[str] = "%(levelname)s %(name)s – %(message)s"


def configure_logging(namespace: str) -> logging.Logger:
    """
    Configure and return a module-scoped logger.

    Only the first call sets up the root handler; subsequent calls
    re-use it to avoid duplicated lines when libraries recurse.
    """
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(_FMT))
        root.setLevel(logging.INFO)
        root.addHandler(handler)
    return logging.getLogger(namespace)


# ────────────────────────────────────────────────────────────────────────────
# Cache directory
# ────────────────────────────────────────────────────────────────────────────
def cache_dir() -> Path:
    """
    Return ForgeAvatar’s writable cache folder.

    Respects XDG on *nix; falls back to %LOCALAPPDATA% on Windows.
    """
    base = (
        Path(os.getenv("XDG_CACHE_HOME", ""))  # Linux
        or Path(os.getenv("LOCALAPPDATA", ""))  # Windows
        or Path.home() / ".cache"
    )
    path = base / "forgeavatar"
    path.mkdir(parents=True, exist_ok=True)
    return path


# ────────────────────────────────────────────────────────────────────────────
# Misc helpers
# ────────────────────────────────────────────────────────────────────────────
_SLUG_RE: Final[re.Pattern[str]] = re.compile(r"[^a-zA-Z0-9_-]+")


def slugify(text: str) -> str:
    """Convert *text* into a filesystem-safe slug."""
    return _SLUG_RE.sub("_", text).strip("_").lower()


def ensure_dir(path: str | Path) -> None:
    """Create *path* (and parents) if missing."""
    Path(path).mkdir(parents=True, exist_ok=True)


def infer_output_filename(
    input_path: str | Path,
    *,
    suffix: str = "_out",
    ext: Optional[str] = None,
) -> str:
    """
    Build an output filename based on *input_path* plus *suffix*.

    If *ext* is None, keep original extension.
    """
    in_path = Path(input_path)
    new_ext = ext or in_path.suffix
    return str(in_path.with_name(in_path.stem + suffix).with_suffix(new_ext))
