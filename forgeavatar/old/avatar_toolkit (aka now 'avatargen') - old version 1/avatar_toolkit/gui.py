# gui.py
"""Graphical user interface for the Avatar Generator toolkit."""

import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import threading
import os

from .core import run_single
from .config import DEFAULTS
from .utils.face_detect import crop_to_face_or_center

class AvatarGUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Avatar Generator")
        self.image_path = None
        self.result_image = None

        self.build_widgets()

    def build_widgets(self):
        self.preview_label = tk.Label(self.root, text="Drop an image here", width=80, height=20, bg="gray90")
        self.preview_label.pack(padx=10, pady=10)
        self.preview_label.drop_target_register(DND_FILES)
        self.preview_label.dnd_bind('<<Drop>>', self.on_file_dropped)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Open Image", command=self.open_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(self.root, text="Ready", anchor="w")
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

    def open_file(self):
        file = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp")])
        if file:
            self.load_image(file)

    def on_file_dropped(self, event):
        path = event.data.strip("{}").replace('\\', '/')
        self.load_image(path)

    def load_image(self, path):
        self.image_path = path
        self.status.config(text=f"Loading {os.path.basename(path)}...")
        thread = threading.Thread(target=self.process_and_display)
        thread.start()

    def process_and_display(self):
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

    def save_image(self):
        if not self.result_image:
            messagebox.showwarning("No Image", "Process an image first.")
            return
        out_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("WebP", "*.webp")])
        if out_path:
            self.result_image.save(out_path)
            self.status.config(text=f"Saved to {out_path}")

    def run(self):
        self.root.mainloop()


def launch_gui():
    """Launch the GUI application."""
    gui = AvatarGUI()
    gui.run()
