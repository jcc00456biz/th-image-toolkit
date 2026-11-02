#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def compute_image_sharpness(image_path: Path) -> float | None:
    """Measure image sharpness using Laplacian variance.

    Higher values indicate sharper images.

    Args:
        image_path: Path to the image.

    Returns:
        Laplacian variance, or None if the image cannot be processed.
    """
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        with open(image_path, "rb") as f:
            chunk = np.frombuffer(f.read(), dtype=np.uint8)
        img_gray = cv2.imdecode(chunk, cv2.IMREAD_GRAYSCALE)

        if img_gray is None:
            logger.error(f"Failed to load image for sharpness: {image_path}")
            return None

        # Calculate the Laplacian variance.
        laplacian_var = float(cv2.Laplacian(img_gray, cv2.CV_64F).var())
        return laplacian_var

    except Exception as e:
        logger.error(f"Failed to compute sharpness for {image_path}: {e}")
        return None
