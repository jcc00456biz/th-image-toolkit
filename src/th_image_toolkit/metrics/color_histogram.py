#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import logging
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


def compute_color_histogram(image_path: Path) -> list[int] | None:
    """Compute a 768-bin RGB histogram for an image.

    Args:
        image_path: Path to the image.

    Returns:
        A list of 768 histogram values, or None if processing fails.
    """
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        # Read bytes first to support Japanese paths on Windows.
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        with Image.open(io.BytesIO(image_bytes)) as opened_img:
            rgb_img = opened_img.convert(
                "RGB"
            )  # Keep the variable name distinct to avoid reassignment.
            hist = rgb_img.histogram()  # A list of 768 elements
            # Cast explicitly for type checkers.
            return [int(x) for x in hist]

    except Exception as e:
        logger.error(
            f"Failed to compute color histogram for {image_path}: {e}"
        )
        return None
