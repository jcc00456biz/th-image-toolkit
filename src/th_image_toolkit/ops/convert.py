#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from th_image_toolkit.core import (
    IM_COMMON_PARAMS,
    IM_JPEG_PARAMS,
    IM_PNG_PARAMS,
    OutputFormat,
    run_magick,
)
from th_image_toolkit.utils import SUPPORTED_EXTENSIONS

logger = logging.getLogger(__name__)


class ImageConversionError(Exception):
    """Raised when image format conversion fails."""


def convert_image_format(
    src_path: Path,
    dest_path: Path,
    output_format: OutputFormat = OutputFormat.JPEG,
) -> bool:
    """Convert an image to the requested format.

    Args:
        src_path: Path to the source image.
        dest_path: Path for the converted image.
        output_format: Output format, either JPEG or PNG.

    Returns:
        True if conversion succeeds; otherwise, False.
    """
    if not src_path.exists():
        logger.error(f"Source image not found: {src_path}")
        return False

    if src_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        logger.error(f"Unsupported input extension: {src_path.suffix}")
        return False

    # Ensure the destination directory exists.
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Build the command arguments.
    cmd_args = [str(src_path)] + list(IM_COMMON_PARAMS)

    if output_format is OutputFormat.JPEG:
        cmd_args.extend(list(IM_JPEG_PARAMS))
    elif output_format is OutputFormat.PNG:
        cmd_args.extend(list(IM_PNG_PARAMS))
    else:
        logger.error(f"Unsupported output format: {output_format}")
        return False

    cmd_args.append(str(dest_path))

    logger.info(
        f"Converting image format: {src_path.name} -> "
        f"{dest_path.name} ({output_format})"
    )

    try:
        run_magick(cmd_args)
    except Exception as e:
        logger.error(
            f"Failed to convert {src_path.name} to {output_format}: {e}"
        )
        return False

    return True
