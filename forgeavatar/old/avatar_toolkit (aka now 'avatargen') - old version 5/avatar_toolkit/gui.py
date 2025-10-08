from __future__ import annotations

"""avatar_toolkit/gui.py - Graphical user interface for the Avatar Generator toolkit.

Responsibilities:
• Provide a GUI for loading and processing images
• Support drag-and-drop and file dialogs
"""
__version__ = "1.0.0"
__all__ = ["AvatarApp", "launch_gui"]

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import logging
import os
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

from .core import run_single
from .config import DEFAULTS
from .face_detect import FaceDetector
from .utils import ensure_dir

logger = logging.getLogger(__name__)

class AvatarApp:
    """Main application class for the Avatar GUI."""
    def __init__(self) -> None:
        self.root = TkinterDnD.Tk()
        self.root.title("Avatar Generator")

        # Widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(
            self.frame, text="Load Image", command=self.load_image
        )
        self.load_button.pack(pady=10)

        self.image_label = tk.Label(self.frame)
        self.image_label.pack()

        self.process_button = tk.Button(
            self.frame, text="Generate Avatar", command=self.generate_avatar
        )
        self.process_button.pack(pady=10)

        self.status = tk.Label(self.frame, text="", fg="green")
        self.status.pack(pady=5)

        # Face detector
        self.detector = FaceDetector()

        # Bind drag-and-drop
        self.image_label.drop_target_register(DND_FILES)
        self.image_label.dnd_bind('<<Drop>>', self.on_drop)

        self.loaded_image: Image.Image | None = None
        self.result_image: Image.Image | None = None

    def load_image(self) -> None:
        """Open file dialog to select an image."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")]
        )
        if not file_path:
            return
        self._display_image(file_path)

    def on_drop(self, event) -> None:
        """Handle file dropped onto the GUI."""
        file_path = event.data.strip('{}')
        self._display_image(file_path)

    def _display_image(self, file_path: str) -> None:
        """Display the image in the GUI."""
        try:
            img = Image.open(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open image: {e}")
            return
        self.loaded_image = img
        img_tk = ImageTk.PhotoImage(img.resize((300, 300), Image.LANCZOS))
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk
        self.status.config(text=f"Loaded {os.path.basename(file_path)}")

    def generate_avatar(self) -> None:
        """Process the loaded image and display/save the result."""
        if self.loaded_image is None:
            messagebox.showwarning("No image", "Please load an image first.")
            return
        config = DEFAULTS.copy()
        avatar = run_single(self.loaded_image, None, config, return_image=True)
        if avatar is None:
            return
        self.result_image = avatar
        avatar_tk = ImageTk.PhotoImage(
            avatar.resize((300, 300), Image.LANCZOS)
        )
        self.image_label.configure(image=avatar_tk)
        self.image_label.image = avatar_tk
        self.status.config(text="Avatar generated")

    def run(self) -> None:
        """Start the GUI event loop."""
        self.root.mainloop()

def launch_gui() -> None:
    """Launch the GUI application."""
    app = AvatarApp()
    app.run()
