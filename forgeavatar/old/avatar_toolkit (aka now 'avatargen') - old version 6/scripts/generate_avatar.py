#!/usr/bin/env python3
# Generate a single avatar from an image using Avatar Generator CLI
from pathlib import Path
import subprocess
import sys

def main() -> None:
    """Main generate avatar script."""
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    subprocess.run([
        sys.executable, '-m', 'avatargen',
        '--input', str(input_file),
        '--output', str(output_file)
    ])

if __name__ == '__main__':
    main()
