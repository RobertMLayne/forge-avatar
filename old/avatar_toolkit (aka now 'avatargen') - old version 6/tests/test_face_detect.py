# tests/test_face_detect.py
import unittest
import numpy as np
import cv2
from avatar_toolkit.face_detect import detect_face

class TestFaceDetection(unittest.TestCase):
    def test_detect_face_no_face(self):
        blank = np.zeros((200, 200, 3), dtype=np.uint8)
        x, y, w, h = detect_face(blank)
        self.assertEqual((x, y, w, h), (0, 0, 200, 200))
