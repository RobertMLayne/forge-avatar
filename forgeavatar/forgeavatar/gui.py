# ────────────────────────────────────────────────────────────────────────────
# gui.py
#
# • Minimal TkinterDnD drag-and-drop GUI wrapper
# • Exposes launch_gui() for CLI switch
# • Checkbox toggles quality boost pipeline
# ────────────────────────────────────────────────────────────────────────────
from __future__ import annotations

import logging
import threading
from pathlib import Path
from tkinter import BooleanVar, filedialog, ttk

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

from forgeavatar.config import DEFAULT_CONFIG
from forgeavatar.core import run_single
from forgeavatar.processing import process_image
from forgeavatar.utils import configure_logging, slugify

logger = configure_logging(__name__)

__all__: list[str] = ["launch_gui"]

_PREVIEW_W = 400
_PREVIEW_H = 400


class AvatarGUI:
    """Simple drag-and-drop window."""

    def __init__(self) -> None:
        self.root: TkinterDnD.Tk = TkinterDnD.Tk()
        self.root.title("ForgeAvatar")

        # Checkbox – quality boost
        self.quality_var = BooleanVar(value=True)
        ttk.Checkbutton(
            self.root,
            text="Quality boost (SR + face + colour)",
            variable=self.quality_var,
        ).pack(anchor="w", padx=8, pady=4)

        # Canvas preview
        self.preview = tk.Label(self.root, text="Drop image here")
        self.preview.pack(expand=True, fill="both", padx=10, pady=10)
        self.preview.drop_target_register(DND_FILES)
        self.preview.dnd_bind("<<Drop>>", self._on_drop)

        ttk.Button(self.root, text="Save…", command=self._save).pack(pady=4)

        self.current_img: Image.Image | None = None

    # ------------------------------------------------------------------
    def run(self) -> None:
        self.root.mainloop()

    # ------------------------------------------------------------------
    def _on_drop(self, event) -> None:  # type: ignore[override]
        path = Path(event.data.strip("{}"))
        logger.info("Dropped %s", path)
        threading.Thread(target=self._process, args=(path,)).start()

    def _process(self, path: Path) -> None:
        img = Image.open(path).convert("RGBA")
        cfg = DEFAULT_CONFIG.copy()
        if not self.quality_var.get():
            cfg.update({"sr_scale": 1, "face_restore": False, "color_fix": False})
        result = process_image(img, cfg)
        self.current_img = result
        prev = result.resize((_PREVIEW_W, _PREVIEW_H), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(prev)  # keep ref
        self.preview.configure(image=self.tk_img, text="")

    def _save(self) -> None:
        if self.current_img is None:
            return
        fname = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("WebP", "*.webp"), ("JPEG", "*.jpg")],
        )
        if fname:
            self.current_img.save(fname)
            logger.info("Saved → %s", fname)


def launch_gui() -> None:
    """Blocking call to start the GUI."""
    AvatarGUI().run()
