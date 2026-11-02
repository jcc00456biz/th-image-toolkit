#!/usr/init/env python3
# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from th_image_toolkit.core import IM_COMMON_PARAMS, run_magick
from th_image_toolkit.utils import SUPPORTED_EXTENSIONS

logger = logging.getLogger(__name__)


class ImageLevelError(Exception):
    """Raised when auto level adjustment fails."""


def apply_auto_levels(src_path: Path, dest_path: Path) -> Path:
    """Apply automatic level correction and save the result.

    Args:
        src_path: Path to the source image.
        dest_path: Path for the adjusted image.

    Returns:
        The destination path.

    Raises:
        FileNotFoundError: If the source image does not exist.
        ValueError: If the source extension is unsupported.
        ImageLevelError: If ImageMagick fails to process the image.
    """
    if not src_path.exists():
        logger.error(f"Source image not found: {src_path}")
        raise FileNotFoundError(f"Source image not found: {src_path}")

    if src_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        logger.error(f"Unsupported input extension: {src_path.suffix}")
        raise ValueError(f"Unsupported input extension: {src_path.suffix}")

    # Ensure the destination directory exists.
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    cmd_args = [str(src_path)] + list(IM_COMMON_PARAMS)
    cmd_args.append("-auto-level")
    cmd_args.append(str(dest_path))

    logger.info(f"Applying auto-levels: {src_path.name} -> {dest_path.name}")

    try:
        run_magick(cmd_args)
    except Exception as e:
        logger.error(f"Failed to apply auto-levels to {src_path.name}: {e}")
        raise ImageLevelError(f"Failed to apply auto-levels: {e}") from e

    return dest_path
