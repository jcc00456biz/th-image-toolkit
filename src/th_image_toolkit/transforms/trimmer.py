#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画像のエッジおよび周辺色分布を解析し、無劣化でスマートトリミングを行うモジュール。"""

from PIL import Image, ImageOps

# --- 定数定義 ---
DEFAULT_MARGIN_CHECK_SIZE = 64  # 4辺の周辺色分布をサンプリングする幅

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


def _check_image_size(img: Image.Image, margin_size: int) -> bool:
    """画像サイズがサンプリングサイズに対して十分な大きさか検証するガード節。"""
    width, height = img.size
    if width < (margin_size * 2) or height < (margin_size * 2):
        return False
    return True


def _determine_unused_marker_color(
    rgb_img: Image.Image, margin_size: int
) -> tuple[int, int, int] | None:
    """画像の4辺周辺の色分布をサンプリングし、画像内で使用されていない純色を動的に決定する。"""
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
    """パディングされた画像の外側からマーカー色をスキャンし、各辺の限界座標を特定する。"""
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
    """画像周辺の色分布から動的に純色マーカーを決定し、えぐれの頂点を基準に無劣化でトリミングを行う。"""
    if not _check_image_size(img, margin_size):
        return img

    rgb_img = img.convert("RGB")
    marker_color = _determine_unused_marker_color(rgb_img, margin_size)

    if marker_color is None:
        return img

    pad_size = 2
    padded_img = ImageOps.expand(img, border=pad_size, fill=marker_color)

    left, top, right, bottom = _find_boundaries(
        padded_img, marker_color, pad_size
    )

    if left >= right or top >= bottom:
        return img

    return img.crop((left, top, right, bottom))
