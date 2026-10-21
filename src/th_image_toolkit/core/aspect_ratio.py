#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import StrEnum
import io
from pathlib import Path
from PIL import Image, UnidentifiedImageError


class ImageOrientation(StrEnum):
    """Enumeration of image aspect-ratio orientations."""

    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    SQUARE = "square"


def get_image_orientation(image_path: Path) -> ImageOrientation:
    """Return the ImageOrientation for the given image path.

    Classifies the image as portrait, landscape, or square.
    Paths that contain non-ASCII characters (including Japanese) are supported.
    """
    if not image_path.exists():
        raise FileNotFoundError(f"File not found: {image_path}")

    try:
        # Read as binary, then open from memory (workaround for non-ASCII paths on Windows).
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
