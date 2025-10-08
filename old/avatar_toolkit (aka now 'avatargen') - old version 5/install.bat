@echo off
python -m venv .venv
call .\.venv\Scripts\activate
pip install -U pip
pip install -e .[dev]
echo ✔ Dev environment ready.
