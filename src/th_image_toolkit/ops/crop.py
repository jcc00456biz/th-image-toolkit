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

# サフィックス定義
CROP_SUFFIX: str = "_crop"
SPLIT_LEFT_SUFFIX: str = "_split_l"
SPLIT_RIGHT_SUFFIX: str = "_split_r"
SPLIT_TOP_SUFFIX: str = "_split_t"
SPLIT_BOTTOM_SUFFIX: str = "_split_b"


class SplitOrientation(StrEnum):
    """スプリット（分割）の方向を表す列挙型。"""

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


@dataclass(slots=True)
class CropBox:
    """画像の切り抜き範囲（矩形）を表すデータクラス。
    すべての座標は境界ピクセルを含みます（左上基準、右下を含む）。
    """

    left: int
    upper: int
    right: int
    lower: int


@dataclass(slots=True)
class SplitParams:
    """スプリット分割のパラメータを保持するデータクラス。"""

    position: int  # 垂直の場合はX座標、水平の場合はY座標
    orientation: SplitOrientation = SplitOrientation.VERTICAL


class ImageCropError(Exception):
    """Raised when image cropping fails."""


def generate_cropped_path(
    src_path: Path, output_dir: Path | None = None
) -> Path:
    """オリジナルファイル名に対してクロップ用サフィックス（_crop）を付与したパスを生成する。"""
    parent = output_dir if output_dir else src_path.parent
    gen_path = parent / f"{src_path.stem}{CROP_SUFFIX}{src_path.suffix}"
    return generate_safe_filename(gen_path)


def generate_split_paths(
    src_path: Path,
    orientation: SplitOrientation = SplitOrientation.VERTICAL,
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    """オリジナルファイル名に対して分割用のサフィックスを付与したパスを生成する。"""
    parent = output_dir if output_dir else src_path.parent
    stem = src_path.stem
    suffix = src_path.suffix

    if orientation == SplitOrientation.HORIZONTAL:
        suffixes = (SPLIT_TOP_SUFFIX, SPLIT_BOTTOM_SUFFIX)
    else:
        suffixes = (SPLIT_LEFT_SUFFIX, SPLIT_RIGHT_SUFFIX)

    # パスの生成と安全なファイル名への変換をそれぞれに適用してタプルで返す
    return (
        generate_safe_filename(parent / f"{stem}{suffixes[0]}{suffix}"),
        generate_safe_filename(parent / f"{stem}{suffixes[1]}{suffix}"),
    )


def crop_image(
    src_path: Path,
    box: CropBox,
    dest_path: Path | None = None,
) -> Path:
    """指定された CropBox 領域で画像を切り抜き、劣化なしで保存する。

    Args:
        src_path: 入力画像パス
        box: 切り抜き範囲（CropBox。境界のピクセルを含む）
        dest_path: 出力先ファイルのパス（省略時はソースと同じディレクトリに _crop 付きで保存）
    """
    if not src_path.exists():
        logger.error(f"Source image not found: {src_path}")
        raise FileNotFoundError(f"Source image not found: {src_path}")

    if src_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        logger.error(f"Unsupported input extension: {src_path.suffix}")
        raise ValueError(f"Unsupported input extension: {src_path.suffix}")

    # 出力パスが未指定の場合はソースと同じディレクトリに自動生成
    if dest_path is None:
        dest_path = generate_cropped_path(src_path, output_dir=None)

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Pillowの仕様（右・下端が排他）に対応するため、境界ピクセルを含める目的で right/lower に +1 する
    pillow_box = (box.left, box.upper, box.right + 1, box.lower + 1)

    try:
        # Windowsの日本語パス対策としてバイナリ経由で読み込む
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
    """クロップ領域を指定した上で、SplitParams（方向と位置）に基づいて2分割して保存する。

    Args:
        src_path: 入力画像パス
        crop_box: ベースとなるクロップ矩形
        split_params: 分割の方向と位置（SplitParams）
        output_dir: 保存先ディレクトリ（省略時はソースと同じディレクトリに保存）
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

    # 命名規則に従った左右／上下の出力パスを自動生成
    target_first, target_second = generate_split_paths(
        src_path, orientation, output_dir
    )

    saved_first = crop_image(src_path, first_box, dest_path=target_first)
    saved_second = crop_image(src_path, second_box, dest_path=target_second)

    return saved_first, saved_second
