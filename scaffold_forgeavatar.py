#!/usr/bin/env python3
"""
scaffold_forgeavatar.py
• One-shot scaffold generator for a *fresh* ForgeAvatar repo
• Creates every folder / file listed in §2 Repository layout
• Skips existing paths, so safe to re-run
"""

from __future__ import annotations

import shutil
from pathlib import Path

# ───────────────────────────────────────────────────────────────
# Directory / file manifest
# ───────────────────────────────────────────────────────────────
ROOT = Path("forgeavatar").resolve()

DIRS: list[Path] = [
    ROOT / "forgeavatar" / "assets",
    ROOT / "docs",
    ROOT / "tests",
    ROOT / ".github" / "workflows",
    ROOT / "scripts",
]

FILES: dict[Path, str] = {
    # Package skeleton
    ROOT / "forgeavatar" / "__init__.py": '"""Package root."""\n',
    ROOT / "forgeavatar" / "config.py": "",
    ROOT / "forgeavatar" / "utils.py": "",
    ROOT / "forgeavatar" / "superres.py": "",
    ROOT / "forgeavatar" / "face_restore.py": "",
    ROOT / "forgeavatar" / "color_fix.py": "",
    ROOT / "forgeavatar" / "face_detect.py": "",
    ROOT / "forgeavatar" / "processing.py": "",
    ROOT / "forgeavatar" / "core.py": "",
    ROOT / "forgeavatar" / "cli.py": "",
    ROOT / "forgeavatar" / "gui.py": "",
    ROOT / "forgeavatar" / "batch.py": "",
    ROOT / "forgeavatar" / "assets" / "logo.png": "",  # placeholder

    # Docs & community
    ROOT / "docs" / "conf.py": "",
    ROOT / "docs" / "index.rst": "",
    ROOT / "docs" / "usage.rst": "",
    ROOT / "docs" / "api.rst": "",

    ROOT / ".github" / "workflows" / "python.yml": "",
    ROOT / ".github" / "workflows" / "gh-pages.yml": "",

    # Root metadata
    ROOT / "Makefile": "",
    ROOT / "pyproject.toml": "",
    ROOT / "LICENSE": "",
    ROOT / "README.md": "",
    ROOT / "MANIFEST.in": "",
    ROOT / "CODE_OF_CONDUCT.md": "",
    ROOT / "SECURITY.md": "",
    ROOT / "SUPPORT.md": "",
    ROOT / "setup.cfg": "",
    ROOT / "forgeavatar.spec": "",
    ROOT / "install.sh": "",
    ROOT / "install.bat": "",
}

# ───────────────────────────────────────────────────────────────
# Helper functions
# ───────────────────────────────────────────────────────────────
def create_tree() -> None:
    for d in DIRS:
        d.mkdir(parents=True, exist_ok=True)

    for path, content in FILES.items():
        if not path.exists():
            path.write_bytes(content.encode("utf-8") if content else b"")
        elif path.is_file() and content:
            # Preserve existing non-empty files
            print(f"skip (exists): {path.relative_to(ROOT)}")

    # Add .gitkeep into empty folders for version control
    for d in DIRS:
        if not any(d.iterdir()):
            (d / ".gitkeep").touch()

    print("ForgeAvatar scaffold complete ✔")


def nuke_tree() -> None:
    """Danger: delete entire scaffold root (for fresh re-runs)."""
    if ROOT.exists():
        shutil.rmtree(ROOT)
        print("Removed existing forgeavatar tree.")


# ───────────────────────────────────────────────────────────────
# Main
# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    create_tree()
