#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import logging

logger = logging.getLogger(__name__)


def get_image_resolution(image_path: Path) -> tuple[int, int] | None:
    """Get an image's dimensions.

    Args:
        image_path: Path to the image.

    Returns:
        A (width, height) pair, or None if the image cannot be read.
    """
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        with Image.open(io.BytesIO(image_bytes)) as img:
            width, height = img.size
            return width, height

    except (UnidentifiedImageError, OSError) as e:
        logger.error(f"Failed to get resolution for {image_path}: {e}")
        return None
