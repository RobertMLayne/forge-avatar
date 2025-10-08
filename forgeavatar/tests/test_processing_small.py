"""Processing-stage smoke-test (CPU-only)."""
from __future__ import annotations

import unittest

from PIL import Image

from forgeavatar.processing import process_image

CFG = {
    "sr_scale": 2,
    "face_restore": False,  # keep test fast / no GFPGAN
    "color_fix": False,
    "bezel": 0,
    "drop_shadow": False,
}


class TestProcessing(unittest.TestCase):
    def test_output_banner_size(self) -> None:
        small = Image.new("RGB", (64, 64), "green")
        out = process_image(small, CFG)
        self.assertEqual(out.size, (1_584, 396))
