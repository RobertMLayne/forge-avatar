# ForgeAvatar <img src="forgeavatar/assets/logo.png" width="42" />

Remaster tiny, blurry profile pictures into studio-quality avatars.

| Windows 11 | macOS | Linux |
| ---------- | ----- | ----- |
| ✅ first-class | ✅ | ✅ |

---

## Features 🚀

* **Super-resolution** (Real-ESRGAN ↔ OpenCV fallback)
* **GFPGAN** face clean-up (optional)
* **Auto colour revival** (white-balance + CLAHE)
* Gold-black-gold bezel, rounded-rectangle mask, drop shadow
* Drag-and-drop GUI with live preview
* Threaded batch mode
* Wheels, PyInstaller EXE, and docs deploy via GitHub Actions

---

## Installation

```bash
pip install forgeavatar          # core features
pip install realesrgan gfpgan    # (optional) extra quality
