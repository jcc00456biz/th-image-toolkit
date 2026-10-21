#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import logging
from pathlib import Path

import imagehash  # type: ignore
from PIL import Image

logger = logging.getLogger(__name__)


def compute_phash(image_path: Path) -> str | None:
    """指定画像のパーセプトアルハッシュ（pHash）を求める（日本語パス対応）。"""
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        # バイナリとして読み込んでからメモリ上の画像として開く（Windowsの日本語パス対策）
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        with Image.open(io.BytesIO(image_bytes)) as img:
            phash = imagehash.phash(img)
            return str(phash)

    except Exception as e:
        logger.error(f"Failed to compute pHash for {image_path}: {e}")
        return None
