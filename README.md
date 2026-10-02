# ForgeAvatar <img src="forgeavatar/assets/logo.png" width="42" />

Remaster tiny, blurry profile pictures into studio-quality avatars.

This preserved source repository has incomplete packaging and documentation
scaffolds. Its historical GitHub Actions files were empty; automated wheels,
Windows EXE builds and documentation deployment are unverified. Read the
[workflow status](docs/WORKFLOW-STATUS.md) and the maintained
[Avatar Suite feature coverage](https://github.com/RobertMLayne/avatar-suite/blob/main/docs/FEATURE-COVERAGE.md)
before relying on the build or platform claims below.

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
* Wheels, PyInstaller EXE, and docs deployment remain unresolved

---

## Installation

```bash
pip install forgeavatar          # core features
pip install realesrgan gfpgan    # (optional) extra quality
