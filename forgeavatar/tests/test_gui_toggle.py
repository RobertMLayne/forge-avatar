"""Mocked GUI checkbox alters config."""
from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from forgeavatar.gui import AvatarGUI


class TestGuiToggle(unittest.TestCase):
    @patch("forgeavatar.gui.process_image")
    @patch("forgeavatar.gui.Image.open")
    def test_quality_checkbox(self, mock_open, mock_proc) -> None:
        gui = AvatarGUI()
        gui.quality_var.set(False)  # disable quality boost
        fake_path = MagicMock()
        gui._process(fake_path)
        cfg_used = mock_proc.call_args.args[1]
        self.assertEqual(cfg_used["sr_scale"], 1)
        self.assertFalse(cfg_used["face_restore"])
