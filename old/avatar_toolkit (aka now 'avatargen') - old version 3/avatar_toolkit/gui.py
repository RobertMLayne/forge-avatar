from __future__ import annotations

"""
avatar_toolkit/gui.py - Graphical user interface for the Avatar Generator toolkit.

Responsibilities:
- Provide a GUI for loading and processing images
- Support drag-and-drop and file dialogs
"""

__version__ = "1.0.0"
__all__ = ["AvatarApp", "launch_gui"]

import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import os
from PIL import Image, ImageTk

from .core import run_single
from .config import DEFAULTS
from .face_detect import crop_to_face_or_center


class AvatarApp:
    def __init__(self, root: tk.Tk | None = None) -> None:
        """Initialize the Avatar GUI application."""
        if root is None:
            # Use the TkinterDnD root for drag-and-drop support
            self.root = TkinterDnD.Tk()
        else:
            self.root = root
        self.root.title("Avatar Generator")
        self.image_path: str | None = None
        self.result_image: Image.Image | None = None

        self.build_widgets()

    def build_widgets(self) -> None:
        self.preview_label = tk.Label(
            self.root, text="Drop an image here", width=80, height=20, bg="gray90"
        )
        self.preview_label.pack(padx=10, pady=10)
        self.preview_label.drop_target_register(DND_FILES)
        self.preview_label.dnd_bind('<<Drop>>', self.on_file_dropped)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Open Image", command=self.open_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(self.root, text="Ready", anchor="w")
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def open_file(self) -> None:
        file = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp")])
        if file:
            self.load_image(file)

    def on_file_dropped(self, event: tk.Event) -> None:
        path = event.data.strip('{}').replace('\\', '/')
        self.load_image(path)

    def load_image(self, path: str) -> None:
        self.image_path = path
        self.status.config(text=f"Loading {os.path.basename(path)}...")
        thread = threading.Thread(target=self.process_and_display)
        thread.start()

    def process_and_display(self) -> None:
        try:
            result = run_single(self.image_path, output_path=None, config=DEFAULTS, return_image=True)
            result = crop_to_face_or_center(result)
            self.result_image = result
            img = result.copy().resize((256, 256), Image.LANCZOS)
            preview = ImageTk.PhotoImage(img)
            self.preview_label.config(image=preview)
            self.preview_label.image = preview
            self.status.config(text=f"Processed: {os.path.basename(self.image_path)}")
        except Exception as e:
            self.status.config(text=f"Error: {str(e)}")

    def save_image(self) -> None:
        if not self.result_image:
            messagebox.showwarning("No Image", "Process an image first.")
            return
        out_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("WebP", "*.webp")],
        )
        if out_path:
            self.result_image.save(out_path)
            self.status.config(text=f"Saved to {out_path}")

    def run(self) -> None:
        self.root.mainloop()


def launch_gui() -> None:
    """Launch the GUI application."""
    app = AvatarApp()
    app.run()
