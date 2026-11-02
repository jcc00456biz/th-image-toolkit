#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import logging
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from th_image_toolkit.utils import (
    SUPPORTED_EXTENSIONS,
    generate_safe_filename,
)

logger = logging.getLogger(__name__)

# Output filename suffixes.
CROP_SUFFIX: str = "_crop"
SPLIT_LEFT_SUFFIX: str = "_split_l"
SPLIT_RIGHT_SUFFIX: str = "_split_r"
SPLIT_TOP_SUFFIX: str = "_split_t"
SPLIT_BOTTOM_SUFFIX: str = "_split_b"


class SplitOrientation(StrEnum):
    """Direction used to split an image."""

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


@dataclass(slots=True)
class CropBox:
    """Crop rectangle with inclusive boundary coordinates."""

    left: int
    upper: int
    right: int
    lower: int


@dataclass(slots=True)
class SplitParams:
    """Parameters for splitting an image.

    Attributes:
        position: X coordinate for vertical splits or Y coordinate for horizontal splits.
        orientation: Direction of the split.
    """

    position: int  # X for vertical splits; Y for horizontal splits.
    orientation: SplitOrientation = SplitOrientation.VERTICAL


class ImageCropError(Exception):
    """Raised when image cropping fails."""


def generate_cropped_path(
    src_path: Path, output_dir: Path | None = None
) -> Path:
    """Create a crop output path using the source filename.

    Args:
        src_path: Path to the source image.
        output_dir: Optional directory for the output.

    Returns:
        A safe path for the cropped image.
    """
    parent = output_dir if output_dir else src_path.parent
    gen_path = parent / f"{src_path.stem}{CROP_SUFFIX}{src_path.suffix}"
    return generate_safe_filename(gen_path)


def generate_split_paths(
    src_path: Path,
    orientation: SplitOrientation = SplitOrientation.VERTICAL,
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Create output paths for the two split images.

    Args:
        src_path: Path to the source image.
        orientation: Direction of the split.
        output_dir: Optional directory for the outputs.

    Returns:
        Paths for the first and second split images.
    """
    parent = output_dir if output_dir else src_path.parent
    stem = src_path.stem
    suffix = src_path.suffix

    if orientation == SplitOrientation.HORIZONTAL:
        suffixes = (SPLIT_TOP_SUFFIX, SPLIT_BOTTOM_SUFFIX)
    else:
        suffixes = (SPLIT_LEFT_SUFFIX, SPLIT_RIGHT_SUFFIX)

    # Sanitize and return both output paths.
    return (
        generate_safe_filename(parent / f"{stem}{suffixes[0]}{suffix}"),
        generate_safe_filename(parent / f"{stem}{suffixes[1]}{suffix}"),
    )


def crop_image(
    src_path: Path,
    box: CropBox,
    dest_path: Path | None = None,
) -> Path:
    """Crop an image to the specified box and save it without re-encoding.

    Args:
        src_path: Path to the source image.
        box: Crop rectangle with inclusive boundary pixels.
        dest_path: Output path; defaults to a suffixed file beside the source.

    Returns:
        Path to the saved crop.

    Raises:
        FileNotFoundError: If the source image does not exist.
        ValueError: If the source extension is unsupported.
        ImageCropError: If the image cannot be opened or cropped.
    """
    if not src_path.exists():
        logger.error(f"Source image not found: {src_path}")
        raise FileNotFoundError(f"Source image not found: {src_path}")

    if src_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        logger.error(f"Unsupported input extension: {src_path.suffix}")
        raise ValueError(f"Unsupported input extension: {src_path.suffix}")

    # Generate a default output path if none was provided.
    if dest_path is None:
        dest_path = generate_cropped_path(src_path, output_dir=None)

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Pillow excludes right and lower bounds, so add one to include them.
    pillow_box = (box.left, box.upper, box.right + 1, box.lower + 1)

    try:
        # Read bytes first to support paths with non-ASCII characters.
        with open(src_path, "rb") as f:
            image_bytes = f.read()

        with Image.open(io.BytesIO(image_bytes)) as opened_img:
            cropped_img = opened_img.crop(pillow_box)
            save_format = opened_img.format
            cropped_img.save(dest_path, format=save_format)

    except (UnidentifiedImageError, OSError) as e:
        logger.error(f"Failed to open or process image {src_path.name}: {e}")
        raise ImageCropError(f"Failed to crop image: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error during cropping {src_path.name}: {e}")
        raise ImageCropError(f"Unexpected crop error: {e}") from e

    logger.info(
        f"Cropped image: {src_path.name} -> {dest_path.name} (box={box})"
    )
    return dest_path


def split_and_crop_image(
    src_path: Path,
    crop_box: CropBox,
    split_params: SplitParams,
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Crop a region, split it, and save both resulting images.

    Args:
        src_path: Path to the source image.
        crop_box: Base crop rectangle to split.
        split_params: Split direction and position.
        output_dir: Output directory; defaults to the source directory.

    Returns:
        Paths to the two saved image sections.

    Raises:
        FileNotFoundError: If the source image does not exist.
        ValueError: If the source extension is unsupported.
        ImageCropError: If either section cannot be cropped.
    """
    pos = split_params.position
    orientation = split_params.orientation

    if orientation == SplitOrientation.HORIZONTAL:
        clamped_pos = max(crop_box.upper, min(pos, crop_box.lower))
        first_box = CropBox(
            left=crop_box.left,
            upper=crop_box.upper,
            right=crop_box.right,
            lower=clamped_pos,
        )
        second_box = CropBox(
            left=crop_box.left,
            upper=clamped_pos,
            right=crop_box.right,
            lower=crop_box.lower,
        )
    else:
        clamped_pos = max(crop_box.left, min(pos, crop_box.right))
        first_box = CropBox(
            left=crop_box.left,
            upper=crop_box.upper,
            right=clamped_pos,
            lower=crop_box.lower,
        )
        second_box = CropBox(
            left=clamped_pos,
            upper=crop_box.upper,
            right=crop_box.right,
            lower=crop_box.lower,
        )

    # Generate output paths based on the split direction.
    target_first, target_second = generate_split_paths(
        src_path, orientation, output_dir
    )

    saved_first = crop_image(src_path, first_box, dest_path=target_first)
    saved_second = crop_image(src_path, second_box, dest_path=target_second)

    return saved_first, saved_second
