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
    """
    指定された画像ファイルを入力形式に問わず、
    指定された OutputFormat (JPEG / PNG) に変換し、
    最適化パラメータ（ハフマン最適化や圧縮フィルタ等）を適用して
    dest_path へ保存する。
    """
    if not src_path.exists():
        logger.error(f"Source image not found: {src_path}")
        return False

    if src_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        logger.error(f"Unsupported input extension: {src_path.suffix}")
        return False

    # 出力先ディレクトリの確実な作成
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # コマンドパラメータの組み立て
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
