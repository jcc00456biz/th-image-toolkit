#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from PIL import Image

from th_image_toolkit.core import (
    IM_COMMON_PARAMS,
    IM_UNSHARP_PARAMS,
    run_magick,
)
from th_image_toolkit.utils import SUPPORTED_EXTENSIONS

logger = logging.getLogger(__name__)


class ImageResizeError(Exception):
    """Raised when image resizing or sharpening fails."""


def resize_and_sharpen(
    src_path: Path,
    target_width: int,
    target_height: int,
    dest_path: Path,
    auto_level: bool = False,
) -> Path:
    """
    指定されたサイズへのリサイズ、および自動レベル補正を行う。
    リサイズ元の画像サイズを取得し、拡大方向（目標サイズが元サイズより大きい）の
    場合のみアンシャープマスクを適用して指定された dest_path へ保存する。
    """
    if not src_path.exists():
        logger.error(f"Source image not found: {src_path}")
        raise FileNotFoundError(f"Source image not found: {src_path}")

    if src_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        logger.error(f"Unsupported input extension: {src_path.suffix}")
        raise ValueError(f"Unsupported input extension: {src_path.suffix}")

    # PIL を用いて元画像のサイズを取得し、拡大かどうかを判定
    try:
        with Image.open(src_path) as img:
            src_w, src_h = img.size
    except Exception as e:
        logger.error(
            f"Failed to get image dimensions for {src_path.name}: {e}"
        )
        raise ImageResizeError(
            f"Failed to read source image dimensions: {e}"
        ) from e

    # 目標サイズのどちらかが元サイズを上回っている場合は拡大とみなす
    is_enlargement = (target_width > src_w) or (target_height > src_h)

    # 出力先ディレクトリの確実な作成
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    cmd_args = [str(src_path)] + list(IM_COMMON_PARAMS)

    # 自動レベル補正が有効な場合、コマンド引数に追加
    if auto_level:
        cmd_args.append("-auto-level")

    cmd_args.extend(["-resize", f"{target_width}x{target_height}!"])

    # 拡大時のみアンシャープパラメータを追加
    if is_enlargement:
        cmd_args.extend(list(IM_UNSHARP_PARAMS))

    cmd_args.append(str(dest_path))

    if is_enlargement:
        action_desc = (
            "Resizing (enlargement), auto-leveling and sharpening"
            if auto_level
            else "Resizing (enlargement) and sharpening"
        )
    else:
        action_desc = (
            "Resizing (reduction) and auto-leveling"
            if auto_level
            else "Resizing (reduction)"
        )

    logger.info(
        f"{action_desc}: {src_path.name} "
        f"({src_w}x{src_h} -> "
        f"{target_width}x{target_height}) -> "
        f"{dest_path.name}"
    )

    try:
        run_magick(cmd_args)
    except Exception as e:
        logger.error(
            f"Failed to process resize/sharpen for {src_path.name}: {e}"
        )
        raise ImageResizeError(f"Failed to process resize/sharpen: {e}") from e

    return dest_path
