"""Unit-tests for face_restore (noop when GFPGAN absent)."""
from __future__ import annotations

import importlib
import unittest
from pathlib import Path

from PIL import Image

from forgeavatar.face_restore import restore_face

FIXTURE = Image.new("RGBA", (128, 128), "grey")


class TestFaceRestore(unittest.TestCase):
    def test_noop_or_restored_size_same(self) -> None:
        out = restore_face(FIXTURE)
        self.assertEqual(out.size, FIXTURE.size)

    def test_backend_flag(self) -> None:
        mod = importlib.import_module("forgeavatar.face_restore")
        self.assertTrue(hasattr(mod, "FaceRestorer"))
