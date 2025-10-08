from __future__ import annotations

"""
avatar_toolkit/face_detect.py - Face detection utilities.

Responsibilities:
• Detect faces in images using Haar cascades
• Provide utilities for cropping to faces
"""
__version__ = "1.0.0"
__all__ = ["FaceDetector", "detect_face"]

import logging
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple, Union

import cv2

logger = logging.getLogger(__name__)

class FaceDetector:
    """Face detection using OpenCV Haar cascades."""

    def __init__(
        self,
        model_path: Optional[Union[str, Path]] = None,
        scale_factor: float = 1.1,
        min_neighbors: int = 5,
    ) -> None:
        """
        Initialize the face detector.

        Args:
            model_path: Path to Haar cascade XML file.
                        If None, use default frontal face cascade.
            scale_factor: How much the image size is reduced at each scale.
            min_neighbors: How many neighbors each rectangle should have
                           to retain it.
        """
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors

        # Determine cascade model path
        if model_path:
            cascade_file = str(model_path)
        else:
            # Default to OpenCV's frontal face cascade
            try:
                cascade_file = (
                    cv2.data.haarcascades +
                    "haarcascade_frontalface_default.xml"
                )
            except AttributeError as e:
                logger.exception("OpenCV data path not found: %s", e)
                raise
        self.classifier = cv2.CascadeClassifier(cascade_file)
        if self.classifier.empty():
            logger.error(
                "Failed to load face detector model from %s", cascade_file
            )
            raise ValueError(
                f"Failed to load face detector model from {cascade_file}"
            )
        logger.info("Loaded face detector model: %s", cascade_file)

    def detect_faces(self, image: Union[str, Path, "cv2.UMat", "cv2.Mat"]) -> List[Tuple[int, int, int, int]]:
        """Detect faces in an image and return bounding boxes."""
        # Load image if path provided
        if isinstance(image, (str, Path)):
            img = cv2.imread(str(image))
        else:
            img = image
        if img is None:
            logger.error("Could not load image for face detection: %s", image)
            return []

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.classifier.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors
        )
        boxes: List[Tuple[int, int, int, int]] = []
        for (x, y, w, h) in faces:
            boxes.append((int(x), int(y), int(w), int(h)))
        logger.info("Detected %d face(s)", len(boxes))
        return boxes

    def detect_largest_face(self, image: Union[str, Path, "cv2.UMat", "cv2.Mat"]) -> Tuple[int, int, int, int]:
        """Detect the largest face in an image;
        return (x,y,w,h) or (0,0,0,0) if none."""
        boxes = self.detect_faces(image)
        if not boxes:
            return (0, 0, 0, 0)
        # Return the box with the largest area
        largest = max(boxes, key=lambda rect: rect[2] * rect[3])
        return largest

def detect_face(image: Union[str, Path, "cv2.UMat", "cv2.Mat", np.ndarray]) -> Tuple[int, int, int, int]:
    """Detect the largest face in the image;
    if none, return bounding box of entire image."""
    detector = FaceDetector()
    x, y, w, h = detector.detect_largest_face(image)
    if (w, h) == (0, 0):
        # No face detected; return full image dimensions
        if isinstance(image, (str, Path)):
            img = cv2.imread(str(image))
            if img is None:
                return (0, 0, 0, 0)
        elif isinstance(image, np.ndarray):
            img = image
        else:
            try:
                img = np.array(image)
            except Exception:
                return (0, 0, 0, 0)
        height, width = img.shape[:2]
        return (0, 0, width, height)
    return (x, y, w, h)
