#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import logging
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


def compute_color_histogram(image_path: Path) -> list[int] | None:
    """指定画像の RGB カラーヒストグラムを求める（日本語パス対応）。
    例外は投げず、失敗時は logger に出力して None を返す。
    戻り値は 256bin × 3ch = 768 要素のリスト。
    """
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        # バイナリとして読み込んでからメモリ上の画像として開く（Windowsの日本語パス対策）
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        with Image.open(io.BytesIO(image_bytes)) as opened_img:
            rgb_img = opened_img.convert(
                "RGB"
            )  # 変数名を分けることで再代入エラーを回避
            hist = rgb_img.histogram()  # 768 要素のリスト
            # histogram() は通常 list[int] を返しますが、型チェッカーの補正として明示することも可能です
            return [int(x) for x in hist]

    except Exception as e:
        logger.error(
            f"Failed to compute color histogram for {image_path}: {e}"
        )
        return None
