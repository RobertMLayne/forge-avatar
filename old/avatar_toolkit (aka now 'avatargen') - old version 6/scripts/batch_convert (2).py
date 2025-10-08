#!/usr/bin/env python3
# Batch convert images to avatars using Avatar Generator CLI
from pathlib import Path
import subprocess
import sys

def main() -> None:
    """Main batch convert script."""
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_dir> <output_dir>")
        sys.exit(1)
    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)
    for img_path in input_dir.iterdir():
        if img_path.is_file():
            subprocess.run([
                sys.executable, '-m', 'avatargen',
                '--input', str(img_path),
                '--output', str(output_dir / img_path.name)
            ])

if __name__ == '__main__':
    main()
