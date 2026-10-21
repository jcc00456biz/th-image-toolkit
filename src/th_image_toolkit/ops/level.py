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
    """
    指定された画像ファイルに対して自動レベル補正 (-auto-level) を実行し、
    指定された dest_path へ保存する。
    """
    if not src_path.exists():
        logger.error(f"Source image not found: {src_path}")
        raise FileNotFoundError(f"Source image not found: {src_path}")

    if src_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        logger.error(f"Unsupported input extension: {src_path.suffix}")
        raise ValueError(f"Unsupported input extension: {src_path.suffix}")

    # 出力先ディレクトリの確実な作成
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
