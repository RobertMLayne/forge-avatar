# tests/test_core.py
import os
import unittest
from PIL import Image
from avatargen.core import run_single
from avatargen.config import DEFAULTS

class TestCoreProcessing(unittest.TestCase):
    def setUp(self):
        self.img = Image.new("RGB", (512, 512), color="blue")
        self.output_path = "test_output.png"
        self.config = DEFAULTS.copy()
        self.config["bezel"] = 4
        self.config["output_format"] = "PNG"

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_run_single_generates_output(self):
        run_single(self.img, self.output_path, self.config)
        self.assertTrue(os.path.exists(self.output_path))

if __name__ == "__main__":
    unittest.main()
