#!/usr/bin/env python
"""Standalone script to generate a single avatar from an image file."""
import sys
from avatar_toolkit import core

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_avatar.py <input_image> [output_image]")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        result = core.generate_avatar_file(input_path, output_path)
        print(f"Avatar saved to: {result}")
    except Exception as e:
        print(f"Error generating avatar: {e}")
