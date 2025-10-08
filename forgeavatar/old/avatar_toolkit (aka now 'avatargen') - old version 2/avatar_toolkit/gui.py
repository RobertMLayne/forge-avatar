"""
avatar_toolkit.gui
~~~~~~~~~~~~~~~~~~
Tk/TkinterDnD-based graphical front-end for Avatar Toolkit.
Drag-and-drop is enabled when **tkinterdnd2** is importable; otherwise the GUI
falls back to standard file-open dialogs.

© 2025 Layne Intellectual Property – MIT License
"""

from __future__ import annotations

import logging
import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional

try:  # optional drag-and-drop
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:  # graceful fallback
    DND_FILES = None
    TkinterDnD = None

from PIL import Image, ImageTk

from .config import DEFAULTS
from .processing import process_image
from .utils import ensure_dir
from .core import run_single

log = logging.getLogger(__name__)


class AvatarGUI:
    """Main GUI application class."""

    def __init__(self) -> None:
        # Root window (DnD-aware if possible)
        self.root: tk.Tk = TkinterDnD.Tk() if TkinterDnD else tk.Tk()
        self.root.title("Avatar Toolkit")

        # Display-area label – starts with logo or placeholder text
        self.image_label = tk.Label(
            self.root,
            text="Drop an image or click “Open Image…”",
            bg="#eeeeee",
            width=60,
            height=20,
            anchor="center",
            compound=tk.TOP,
        )
        self.image_label.pack(padx=12, pady=12, fill=tk.BOTH, expand=True)

        # Control buttons
        btn_bar = tk.Frame(self.root)
        btn_bar.pack(pady=6)
        tk.Button(btn_bar, text="Open Image…", command=self._open_dialog).pack(
            side=tk.LEFT, padx=4
        )
        tk.Button(btn_bar, text="Save Avatar As…", command=self._save_dialog).pack(
            side=tk.LEFT, padx=4
        )

        # Drag-and-drop binding (if supported)
        if TkinterDnD:
            self.image_label.drop_target_register(DND_FILES)
            self.image_label.dnd_bind("<<Drop>>", self._on_drop)

        # Runtime state
        self._src_image: Optional[Image.Image] = None     # original
        self._avatar: Optional[Image.Image] = None        # processed
        self._photo_ref: Optional[ImageTk.PhotoImage] = None  # displayed img

        # Try to load logo.png for initial display (non-fatal if absent)
        self._show_logo()

    # ───────────────────────────── helpers ──────────────────────────────

    def _show_logo(self) -> None:
        logo_path = Path(__file__).with_suffix("").parent / "assets" / "logo.png"
        if not logo_path.exists():
            return
        try:
            img = Image.open(logo_path).convert("RGBA").resize((128, 128), Image.LANCZOS)
            self._display_image(img, keep_text=True)
        except Exception as exc:  # pragma: no cover
            log.debug("Logo load failed: %s", exc)

    def _open_dialog(self) -> None:
        ftypes = [("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.gif")]
        path = filedialog.askopenfilename(title="Choose an image", filetypes=ftypes)
        if path:
            self._start_processing(Path(path))

    def _on_drop(self, event) -> None:  # TkinterDnD callback
        try:
            files = self.root.tk.splitlist(event.data)
            self._start_processing(Path(files[0]))
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("Drag-and-Drop Error", str(exc))

    # ───────────────────────── image processing ─────────────────────────

    def _start_processing(self, path: Path) -> None:
        """Load the selected image and kick off processing in a thread."""
        try:
            self._src_image = Image.open(path).convert("RGBA")
        except Exception as exc:
            messagebox.showerror("Open Error", f"Cannot open image:\n{exc}")
            return

        self._display_image(self._src_image)  # quick feedback

        def worker() -> None:
            try:
                cfg = DEFAULTS.copy()
                self._avatar = process_image(self._src_image, cfg)  # heavy work
                self.root.after(0, lambda: self._display_image(self._avatar))
            except Exception as exc:  # pragma: no cover
                self.root.after(
                    0, lambda: messagebox.showerror("Processing Error", str(exc))
                )

        threading.Thread(target=worker, daemon=True).start()

    def _display_image(self, img: Image.Image, *, keep_text: bool = False) -> None:
        """Fit *img* inside the label while maintaining aspect ratio."""
        label_w = self.image_label.winfo_width() or 640
        label_h = self.image_label.winfo_height() or 360
        ratio = min(label_w / img.width, label_h / img.height)
        disp = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)

        self._photo_ref = ImageTk.PhotoImage(disp)
        self.image_label.config(
            image=self._photo_ref,
            text=("Drop an image or click “Open Image…”" if keep_text else ""),
        )

    # ─────────────────────────── saving ────────────────────────────────

    def _save_dialog(self) -> None:
        if self._avatar is None:
            messagebox.showinfo("Nothing to save", "Generate an avatar first.")
            return

        path = filedialog.asksaveasfilename(
            title="Save avatar",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg;*.jpeg"),
                ("WebP", "*.webp"),
            ],
        )
        if not path:
            return

        # Ensure destination dir exists
        ensure_dir(Path(path).parent)

        fmt = (
            "PNG"
            if path.lower().endswith(".png")
            else "JPEG"
            if path.lower().endswith((".jpg", ".jpeg"))
            else "WEBP"
        )
        try:
            run_single(
                self._avatar,
                path,
                {"format": fmt, "quality": DEFAULTS.get("quality", 95)},
            )
            messagebox.showinfo("Saved", f"Avatar written to:\n{path}")
        except Exception as exc:  # pragma: no cover
            messagebox.showerror("Save Error", str(exc))

    # ─────────────────────────── public API ────────────────────────────

    def run(self) -> None:
        """Start the Tk main-loop (blocking)."""
        self.root.mainloop()


# helper for `python -m avatar_toolkit.gui`
def launch_gui() -> None:
    """Entry-point wrapper so CLI can call `avatar_toolkit.gui.launch_gui()`."""
    AvatarGUI().run()


if __name__ == "__main__":  # python -m avatar_toolkit.gui
    launch_gui()
