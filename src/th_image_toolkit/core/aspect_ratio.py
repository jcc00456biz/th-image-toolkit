#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
from enum import StrEnum
from pathlib import Path

from PIL import Image, UnidentifiedImageError


class ImageOrientation(StrEnum):
    """Enumeration of image aspect-ratio orientations."""

    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    SQUARE = "square"


def get_image_orientation(image_path: Path) -> ImageOrientation:
    """Classify an image as portrait, landscape, or square.

    Args:
        image_path: Path to the image.

    Returns:
        The image's orientation.

    Raises:
        FileNotFoundError: If the path does not exist.
        ValueError: If the image cannot be opened.
    """
    if not image_path.exists():
        raise FileNotFoundError(f"File not found: {image_path}")

    try:
        # Read as binary, then open from memory
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        with Image.open(io.BytesIO(image_bytes)) as img:
            width, height = img.size
    except (UnidentifiedImageError, OSError) as e:
        raise ValueError(f"Failed to open image {image_path}: {e}") from e

    if height > width:
        return ImageOrientation.PORTRAIT
    elif width > height:
        return ImageOrientation.LANDSCAPE
    else:
        return ImageOrientation.SQUARE
