"""
Face detection module.
"""
from __future__ import annotations

import cv2
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

__all__ = ["FaceDetector"]

class FaceDetector:
    """
    Face detection using OpenCV Haar cascades.
    """
    def __init__(self, model_path: Optional[Union[str, Path]] = None,
                 scale_factor: float = 1.1, min_neighbors: int = 5) -> None:
        """
        Initialize the face detector.

        Args:
            model_path: Path to Haar cascade XML file. If None, uses default frontalface cascade.
            scale_factor: Parameter specifying how much the image size is reduced at each image scale.
            min_neighbors: Parameter specifying how many neighbors each candidate rectangle should have to retain it.
        """
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors

        # Determine cascade model path
        if model_path:
            cascade_file = str(model_path)
        else:
            # Default to OpenCV's frontal face cascade
            try:
                cascade_file = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            except AttributeError as e:
                logger.exception("OpenCV data path not found: %s", e)
                raise
        # Load the cascade classifier
        self.classifier = cv2.CascadeClassifier(cascade_file)
        if self.classifier.empty():
            logger.error("Failed to load face detector model from %s", cascade_file)
            raise ValueError(f"Failed to load face detector model from {cascade_file}")
        logger.debug("Loaded face detector model: %s", cascade_file)

    def detect_faces(self, image: Union[str, Path, "cv2.UMat", "cv2.Mat"]) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in an image.

        Args:
            image: File path or OpenCV image (numpy array or UMat).

        Returns:
            List of bounding boxes (x, y, w, h) for each detected face.
        """
        # Read image from file if a path is provided
        if isinstance(image, (str, Path)):
            img = cv2.imread(str(image))
            if img is None:
                logger.error("Failed to read image: %s", image)
                raise FileNotFoundError(f"Cannot read image file {image}")
        else:
            img = image

        # Convert to grayscale for detection if needed
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Perform face detection
        faces = self.classifier.detectMultiScale(gray,
                                                 scaleFactor=self.scale_factor,
                                                 minNeighbors=self.min_neighbors)
        boxes: List[Tuple[int, int, int, int]] = []
        for (x, y, w, h) in faces:
            boxes.append((int(x), int(y), int(w), int(h)))
        logger.info("Detected %d face(s)", len(boxes))
        return boxes
