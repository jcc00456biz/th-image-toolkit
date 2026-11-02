#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smart-trim images by analyzing edges and border colors."""

from PIL import Image, ImageChops

# --- Constants ---
DEFAULT_MARGIN_CHECK_SIZE = 64  # Border width to sample on each side.

# # fmt: off
CANDIDATE_PURE_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]
# # fmt: on

__all__ = [
    "smart_trim_image",
    "DEFAULT_MARGIN_CHECK_SIZE",
    "_determine_unused_marker_color",
    "_find_boundaries",
]


def _check_image_size(img: Image.Image, margin_size: int) -> bool:
    """Check that the image is large enough for the sample margins.

    Args:
        img: Image to check.
        margin_size: Border width to sample on each side.

    Returns:
        Whether the image is at least twice the margin size in both dimensions.
    """
    width, height = img.size
    if width < (margin_size * 2) or height < (margin_size * 2):
        return False
    return True


def _determine_unused_marker_color(
    rgb_img: Image.Image, margin_size: int
) -> tuple[int, int, int] | None:
    """Find a solid marker color absent from the sampled image borders.

    Args:
        rgb_img: Image converted to RGB.
        margin_size: Border width to sample on each side.

    Returns:
        An unused RGB color, or None if every candidate is present.
    """
    width, height = rgb_img.size
    used_colors = set()

    for y in range(margin_size):
        for x in range(width):
            used_colors.add(rgb_img.getpixel((x, y)))
            used_colors.add(rgb_img.getpixel((x, height - 1 - y)))

    for x in range(margin_size):
        for y in range(height):
            used_colors.add(rgb_img.getpixel((x, y)))
            used_colors.add(rgb_img.getpixel((width - 1 - x, y)))

    for color in CANDIDATE_PURE_COLORS:
        if color not in used_colors:
            return color

    return None


def _find_boundaries(
    padded_img: Image.Image, marker_color: tuple[int, int, int], pad_size: int
) -> tuple[int, int, int, int]:
    """Scan for marker-color boundaries and return the content bounds.

    Args:
        padded_img: Image padded with the marker color.
        marker_color: RGB color used for padding.
        pad_size: Padding width on each side.

    Returns:
        Content bounds as (left, top, right, bottom).
    """
    width, height = padded_img.size
    rgb_padded = padded_img.convert("RGB")

    top = pad_size
    for y in range(pad_size, height - pad_size):
        found_non_marker = False
        for x in range(pad_size, width - pad_size):
            if rgb_padded.getpixel((x, y)) != marker_color:
                found_non_marker = True
                break
        if found_non_marker:
            top = y
            break

    bottom = height - pad_size
    for y in range(height - pad_size - 1, pad_size - 1, -1):
        found_non_marker = False
        for x in range(pad_size, width - pad_size):
            if rgb_padded.getpixel((x, y)) != marker_color:
                found_non_marker = True
                break
        if found_non_marker:
            bottom = y + 1
            break

    left = pad_size
    for x in range(pad_size, width - pad_size):
        found_non_marker = False
        for y in range(top, bottom):
            if rgb_padded.getpixel((x, y)) != marker_color:
                found_non_marker = True
                break
        if found_non_marker:
            left = x
            break

    right = width - pad_size
    for x in range(width - pad_size - 1, pad_size - 1, -1):
        found_non_marker = False
        for y in range(top, bottom):
            if rgb_padded.getpixel((x, y)) != marker_color:
                found_non_marker = True
                break
        if found_non_marker:
            right = x + 1
            break

    return left - pad_size, top - pad_size, right - pad_size, bottom - pad_size


def smart_trim_image(
    img: Image.Image, margin_size: int = DEFAULT_MARGIN_CHECK_SIZE
) -> Image.Image:
    """Trim marker-colored borders without re-encoding the image.

    Args:
        img: Image to trim.
        margin_size: Border width to sample when selecting a marker color.

    Returns:
        The trimmed image, or the original if no trim is possible.
    """
    if margin_size < 1 or not _check_image_size(img, margin_size):
        return img

    rgb_img = img.convert("RGB")
    width, height = rgb_img.size
    border_colors: dict[tuple[int, ...], int] = {}

    def count_border_pixel(x: int, y: int) -> None:
        pixel = rgb_img.getpixel((x, y))
        if isinstance(pixel, tuple):
            color = tuple(int(channel) for channel in pixel)
            border_colors[color] = border_colors.get(color, 0) + 1

    for y in range(margin_size):
        for x in range(width):
            count_border_pixel(x, y)
            count_border_pixel(x, height - 1 - y)

    for x in range(margin_size):
        for y in range(height):
            count_border_pixel(x, y)
            count_border_pixel(width - 1 - x, y)

    background_color = max(border_colors, key=border_colors.__getitem__)
    background = Image.new("RGB", rgb_img.size, background_color)
    bounds = ImageChops.difference(rgb_img, background).getbbox()

    if bounds is None:
        return img

    return img.crop(bounds)
