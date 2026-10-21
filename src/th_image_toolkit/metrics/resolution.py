#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import logging

logger = logging.getLogger(__name__)


def get_image_resolution(image_path: Path) -> tuple[int, int] | None:
    """指定された画像ファイルの解像度（幅, 高さ）を取得する。
    例外は投げず、失敗時は logger に出力して None を返す（日本語パス対応）。
    """
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        with Image.open(io.BytesIO(image_bytes)) as img:
            width, height = img.size
            return width, height

    except (UnidentifiedImageError, OSError) as e:
        logger.error(f"Failed to get resolution for {image_path}: {e}")
        return None
