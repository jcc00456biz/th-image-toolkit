#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""アニメイラストや印刷原画の線画部分（エッジ成分）に特化した
シャープネスおよびディテール密度を算出するモジュール。
"""

import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def compute_line_art_sharpness(image_path: Path) -> float | None:
    """アニメパッケージや印刷原画の線画（輪郭）の鮮明度を評価する。
    ソベルフィルタを用いてエッジの強度の平均値を算出し、
    線がどれだけシャープに保たれているかを数値化する（日本語パス対応）。
    """
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        with open(image_path, "rb") as f:
            chunk = np.frombuffer(f.read(), dtype=np.uint8)
        img_gray = cv2.imdecode(chunk, cv2.IMREAD_GRAYSCALE)

        if img_gray is None:
            logger.error(
                f"Failed to load image for line sharpness: {image_path}"
            )
            return None

        # ソベルフィルタでX方向・Y方向のエッジ勾配を計算
        sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)

        # エッジの強度（大きさと方向の合成）を算出
        edge_magnitude = np.sqrt(sobelx**2 + sobely**2)

        # エッジ強度の平均値をアニメイラストのシャープネス指標とする
        score = float(np.mean(edge_magnitude))
        return score

    except Exception as e:
        logger.error(f"Failed to compute line sharpness for {image_path}: {e}")
        return None
