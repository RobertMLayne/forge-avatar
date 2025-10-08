from pathlib import Path

for path in sorted(Path(".").rglob("*")):
    if path.is_file():
        print(f"\n--- {path} ---")
        try:
            content = path.read_text(encoding="utf-8").strip()
            print(content)
        except Exception:
            print("[binary or unreadable]")
