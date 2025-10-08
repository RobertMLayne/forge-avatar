# Avatar Toolkit 🚀

**Smart face‑cropper & high‑DPI profile‑image generator — CLI · GUI · Windows‑first**

[![PyPI](https://img.shields.io/pypi/v/avatar-toolkit?color=brightgreen)](https://pypi.org/project/avatar-toolkit/)
[![CI](https://github.com/<USER>/avatar-toolkit/actions/workflows/python-package.yml/badge.svg)](https://github.com/<USER>/avatar-toolkit/actions)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://<USER>.github.io/avatar-toolkit/)
[![License](https://img.shields.io/github/license/<USER>/avatar-toolkit)](LICENSE)

> Retina‑sharp avatars in **one command**
> – Face‑detection · rounded masks & bezels · multithreaded batch · drag‑and‑drop GUI · YAML / JSON themes · PyInstaller EXE.

---

## ✨ Feature Matrix

| Area                 | Highlights                                                        |
| -------------------- | ----------------------------------------------------------------- |
| **Smart cropping**   | OpenCV Haar cascade → per‑face output · centre fallback           |
| **Styling**          | Rounded rectangles / circles · tri‑tone bezel · DPI‑aware scaling |
| **Hi‑DPI ready**     | 1584×396 banner · 256×256 avatar · Windows & macOS DPI‑aware      |
| **Batch & Parallel** | Thread‑pool converter (OpenCV releases GIL)                       |
| **Drag‑and‑drop**    | Tkinter + `tkinterdnd2` — drop files/folders, instant preview     |
| **Profiles**         | YAML / JSON themes (quality, compression, colours, workers …)     |
| **Unified logging**  | `logging` across modules + `--verbose` flag                       |
| **One‑file EXE**     | Windows‑friendly via bundled PyInstaller spec                     |
| **Python ≥ 3.9**     | Modern typing · `pyproject.toml` · Ruff / Black                   |

---

## 🔧 Install

```bash
# Stable release (PyPI)
pip install avatar-toolkit

# Dev clone
git clone https://github.com/<USER>/avatar-toolkit
cd avatar-toolkit
make install            # sets up .venv + dev extras
```

---

## 🚀 Quick CLI

```bash
# Single image → avatars/
avatargen -i photo.jpg -o avatars/

# Batch folder, 8 threads
avatargen -i ./photos -o ./avatars -w 8

# YAML theme
avatargen -i selfie.png -o out/ -c my_theme.yaml

# Launch GUI
avatargen --gui
```

Run `avatargen -h` for all options.

---

## 🖱️ Graphical Interface

```bash
python -m avatar_toolkit.gui
```

1. **Browse** or **drag‑and‑drop** images/folders
2. Pick an output directory
3. *(Optional)* select a YAML/JSON config
4. Hit **Run** — avatars appear, logs stream live

---

## 🐍 Python API

```python
from pathlib import Path
from avatar_toolkit.core import AvatarGenerator

gen = AvatarGenerator()                    # default settings
out_paths = gen.process_image("me.jpg", Path("out"))
print(out_paths)
```

Batch from Python:

```python
from avatar_toolkit import batch
files = ["a.jpg", "b.jpg", "c.jpg"]
batch.process_images(files, "out/", max_workers=6)
```

---

## ⚙️ Profiles (themes)

```yaml
# my_theme.yaml
processing:
  output_format: JPEG
  jpeg_quality: 92
face_detector:
  scale_factor: 1.05
  min_neighbors: 4
batch:
  max_workers: 12
```

```bash
avatargen -i selfies/ -o avatars/ -c my_theme.yaml
```

---

## 📦 One‑file EXE (Windows 11/10)

```bash
make exe                        # builds dist/avatargen.exe
dist/avatargen.exe -i cat.jpg -o out/
```

Great for users without Python.

---

## 🧪 Testing & Coverage

```bash
make test           # pytest -q
make coverage       # pytest --cov avatar_toolkit --cov-report=term-missing
```

CI runs on Windows, macOS, Linux (see *.github/workflows/*).

---

## 📖 Docs

```bash
make docs           # builds docs/_build/html locally
```

Live ➜ **https\://<USER>.github.io/avatar-toolkit/**

---

## 🤝 Contributing

1. Fork & create a feature branch
2. `make format lint test` — keep CI green
3. Open a PR with a concise description

See **CONTRIBUTING.md** for details.

---

## 📝 License

Released under the [MIT License](LICENSE) © 2025‑present Robert M. Layne.
