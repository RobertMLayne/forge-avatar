"""
Avatar Toolkit – top-level package initialiser.

• Exposes an IDE-friendly public API via lazy dynamic exports  
• Keeps heavy sub-modules unloaded until first use (PEP 562)  
• Maintains backward-compat aliases (``DEFAULTS``)  
"""

from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any, Dict

__version__ = "1.0.0"
__all__: list[str]  # populated below

# ───────────────────────────── internal helpers ──────────────────────────────
def _load_exports() -> Dict[str, Any]:
    """Import heavy modules lazily and return the public-symbol map."""
    core = importlib.import_module(".core", __name__)
    proc = importlib.import_module(".processing", __name__)
    cfg = importlib.import_module(".config", __name__)
    gui = importlib.import_module(".gui", __name__)
    cli = importlib.import_module(".cli", __name__)
    batch = importlib.import_module(".batch", __name__)

    return {
        # classes
        "AvatarGenerator": core.AvatarGenerator,
        # functions
        "run_single": core.run_single,
        "process_image": proc.process_image,
        "launch_gui": gui.launch_gui,
        "cli_main": cli.main,
        "run_batch": batch.process_images,
        # constants
        "DEFAULT_CONFIG": cfg.DEFAULT_CONFIG,
        "DEFAULTS": cfg.DEFAULT_CONFIG,  # alias for legacy callers
    }


# ───────────────────────────── lazy attribute hook ───────────────────────────
_exports_cache: Dict[str, Any] | None = None


def __getattr__(name: str) -> Any:  # noqa: D401
    """Resolve ``avatar_toolkit.NAME`` lazily on first access."""
    global _exports_cache
    if _exports_cache is None:
        _exports_cache = _load_exports()
        globals().update(_exports_cache)
    try:
        return globals()[name]
    except KeyError as exc:  # pragma: no cover
        raise AttributeError(
            f"module {__name__!r} has no attribute {name!r}"
        ) from exc


# ─────────────────────────── prime high-frequency attrs ──────────────────────
if _exports_cache is None:
    _exports_cache = _load_exports()
    for _sym in ("run_single", "DEFAULT_CONFIG", "launch_gui"):
        globals()[_sym] = _exports_cache[_sym]

__all__ = sorted(_exports_cache)  # type: ignore[arg-type]

# avoid leaking internals
del _load_exports, ModuleType, Dict, Any, importlib, _sym  # type: ignore
