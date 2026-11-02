#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import logging
from pathlib import Path

import imagehash  # type: ignore
from PIL import Image

logger = logging.getLogger(__name__)


def compute_phash(image_path: Path) -> str | None:
    """Compute an image's perceptual hash.

    Args:
        image_path: Path to the image.

    Returns:
        The hexadecimal pHash string, or None if processing fails.
    """
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        # Read bytes first to support paths with non-ASCII characters.
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        with Image.open(io.BytesIO(image_bytes)) as img:
            phash = imagehash.phash(img)
            return str(phash)

    except Exception as e:
        logger.error(f"Failed to compute pHash for {image_path}: {e}")
        return None
