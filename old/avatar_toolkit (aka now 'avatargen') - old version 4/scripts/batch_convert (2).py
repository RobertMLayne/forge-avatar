#!/usr/bin/env python
"""Standalone script to convert all images in a directory into avatars."""
import sys
from avatar_toolkit import batch

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python batch_convert.py <input_dir> <output_dir>")
        sys.exit(1)
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    try:
        batch.process_directory(input_dir, output_dir)
        print(f"Batch processing complete. Avatars saved to: {output_dir}")
    except Exception as e:
        print(f"Error in batch conversion: {e}")
