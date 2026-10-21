#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def _load_gray(image_path: Path):
    """例外を投げずにグレースケール画像を読み込む（日本語パス対応）"""
    if not image_path.exists():
        logger.error(f"File not found: {image_path}")
        return None

    try:
        # バイナリとして安全に読み込んでからデコードする（日本語パス対策）
        with open(image_path, "rb") as f:
            chunk = np.frombuffer(f.read(), dtype=np.uint8)
        img = cv2.imdecode(chunk, cv2.IMREAD_GRAYSCALE)

        if img is None:
            logger.error(f"Failed to load image: {image_path}")
            return None
        return img
    except Exception as e:
        logger.error(f"Exception while loading image {image_path}: {e}")
        return None


def compute_orb(image_path: Path):
    """ORB 特徴点抽出。例外は投げず None を返す。"""
    img = _load_gray(image_path)
    if img is None:
        return None

    try:
        orb = cv2.ORB_create()  # type: ignore[attr-defined]
        keypoints, descriptors = orb.detectAndCompute(img, None)

        if keypoints is None or descriptors is None:
            logger.error(f"ORB: no keypoints found for {image_path}")
            return None

        return keypoints, descriptors

    except Exception as e:
        logger.error(f"ORB failed for {image_path}: {e}")
        return None


def compute_sift(image_path: Path):
    """SIFT 特徴点抽出。例外は投げず None を返す。"""
    img = _load_gray(image_path)
    if img is None:
        return None

    try:
        sift = cv2.SIFT_create()  # type: ignore[attr-defined]
        keypoints, descriptors = sift.detectAndCompute(img, None)

        if keypoints is None or descriptors is None:
            logger.error(f"SIFT: no keypoints found for {image_path}")
            return None

        return keypoints, descriptors

    except Exception as e:
        logger.error(f"SIFT failed for {image_path}: {e}")
        return None


def compute_akaze(image_path: Path):
    """AKAZE 特徴点抽出。例外は投げず None を返す。"""
    img = _load_gray(image_path)
    if img is None:
        return None

    try:
        akaze = cv2.AKAZE_create()  # type: ignore[attr-defined]
        keypoints, descriptors = akaze.detectAndCompute(img, None)

        if keypoints is None or descriptors is None:
            logger.error(f"AKAZE: no keypoints found for {image_path}")
            return None

        return keypoints, descriptors

    except Exception as e:
        logger.error(f"AKAZE failed for {image_path}: {e}")
        return None
