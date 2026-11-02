#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Measure sharpness and detail in line art."""

import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def compute_line_art_sharpness(image_path: Path) -> float | None:
    """Measure line-art sharpness using the mean Sobel edge magnitude.

    Args:
        image_path: Path to the image.

    Returns:
        Mean edge magnitude, or None if the image cannot be processed.
    """
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        with open(image_path, "rb") as f:
            chunk = np.frombuffer(f.read(), dtype=np.uint8)
        img_gray = cv2.imdecode(chunk, cv2.IMREAD_GRAYSCALE)

        if img_gray is None:
            logger.error(
                f"Failed to load image for line sharpness: {image_path}"
            )
            return None

        # Compute horizontal and vertical edge gradients.
        sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)

        # Combine gradient magnitudes.
        edge_magnitude = np.sqrt(sobelx**2 + sobely**2)

        # Use the mean edge magnitude as the sharpness score.
        score = float(np.mean(edge_magnitude))
        return score

    except Exception as e:
        logger.error(f"Failed to compute line sharpness for {image_path}: {e}")
        return None
