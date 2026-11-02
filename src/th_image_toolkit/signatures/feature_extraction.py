#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def _load_gray(image_path: Path):
    """Load an image as grayscale.

    Args:
        image_path: Path to the image.

    Returns:
        A grayscale image array, or None if loading fails.
    """
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        # Decode bytes to support paths with non-ASCII characters.
        with open(image_path, "rb") as f:
            chunk = np.frombuffer(f.read(), dtype=np.uint8)
        img = cv2.imdecode(chunk, cv2.IMREAD_GRAYSCALE)

        if img is None:
            logger.error(f"Failed to load image: {image_path}")
            return None
        return img
    except Exception as e:
        logger.error(f"Exception while loading image {image_path}: {e}")
        return None


def compute_orb(image_path: Path):
    """Extract ORB keypoints and descriptors.

    Args:
        image_path: Path to the image.

    Returns:
        A (keypoints, descriptors) pair, or None if extraction fails.
    """
    img = _load_gray(image_path)
    if img is None:
        return None

    try:
        orb = cv2.ORB_create()  # type: ignore[attr-defined]
        keypoints, descriptors = orb.detectAndCompute(img, None)

        if keypoints is None or descriptors is None:
            logger.error(f"ORB: no keypoints found for {image_path}")
            return None

        return keypoints, descriptors

    except Exception as e:
        logger.error(f"ORB failed for {image_path}: {e}")
        return None


def compute_sift(image_path: Path):
    """Extract SIFT keypoints and descriptors.

    Args:
        image_path: Path to the image.

    Returns:
        A (keypoints, descriptors) pair, or None if extraction fails.
    """
    img = _load_gray(image_path)
    if img is None:
        return None

    try:
        sift = cv2.SIFT_create()  # type: ignore[attr-defined]
        keypoints, descriptors = sift.detectAndCompute(img, None)

        if keypoints is None or descriptors is None:
            logger.error(f"SIFT: no keypoints found for {image_path}")
            return None

        return keypoints, descriptors

    except Exception as e:
        logger.error(f"SIFT failed for {image_path}: {e}")
        return None


def compute_akaze(image_path: Path):
    """Extract AKAZE keypoints and descriptors.

    Args:
        image_path: Path to the image.

    Returns:
        A (keypoints, descriptors) pair, or None if extraction fails.
    """
    img = _load_gray(image_path)
    if img is None:
        return None

    try:
        akaze = cv2.AKAZE_create()  # type: ignore[attr-defined]
        keypoints, descriptors = akaze.detectAndCompute(img, None)

        if keypoints is None or descriptors is None:
            logger.error(f"AKAZE: no keypoints found for {image_path}")
            return None

        return keypoints, descriptors

    except Exception as e:
        logger.error(f"AKAZE failed for {image_path}: {e}")
        return None
