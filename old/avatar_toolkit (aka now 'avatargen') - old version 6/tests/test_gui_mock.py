# tests/test_gui_mock.py
import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from avatar_toolkit.gui import AvatarApp

class TestGuiDrop(unittest.TestCase):
    @patch("tkinter.Tk")
    def test_gui_initializes(self, mock_tk):
        mock_root = MagicMock(spec=tk.Tk)
        mock_tk.return_value = mock_root
        app = AvatarApp(mock_root)
        self.assertIsNotNone(app)
