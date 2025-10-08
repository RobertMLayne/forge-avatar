"""Unit-tests for colour revival helpers."""
from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image

from forgeavatar.color_fix import auto_white_balance, clahe_lab, revive_colour

FIXTURE = Image.new("RGB", (64, 64), "blue")


class TestColourFix(unittest.TestCase):
    def test_wb_preserves_size(self) -> None:
        out = auto_white_balance(FIXTURE)
        self.assertEqual(out.size, FIXTURE.size)

    def test_clahe_preserves_mode(self) -> None:
        out = clahe_lab(FIXTURE)
        self.assertEqual(out.mode, "RGBA")

    def test_revive_colour_chain(self) -> None:
        out = revive_colour(FIXTURE)
        self.assertEqual(out.size, FIXTURE.size)
