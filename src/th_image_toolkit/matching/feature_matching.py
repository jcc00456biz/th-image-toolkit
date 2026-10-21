#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import logging
from typing import Any

logger = logging.getLogger(__name__)


def match_orb(desc1: Any, desc2: Any):
    """ORB の特徴量を BFMatcher(Hamming) でマッチングする。
    例外は投げず、失敗時は None を返す。
    """
    if desc1 is None or desc2 is None:
        logger.error("ORB descriptors are None")
        return None

    try:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(desc1, desc2)
        matches = sorted(matches, key=lambda x: x.distance)
        return matches

    except Exception as e:
        logger.error(f"ORB matching failed: {e}")
        return None


def match_flann(desc1: Any, desc2: Any):
    """SIFT / AKAZE の特徴量を FLANN(KD-tree) でマッチングする。
    例外は投げず、失敗時は None を返す。
    """
    if desc1 is None or desc2 is None:
        logger.error("FLANN descriptors are None")
        return None

    try:
        index_params = dict(algorithm=1, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(
            index_params, search_params  # type: ignore[arg-type]
        )
        matches = flann.knnMatch(desc1, desc2, k=2)

        # Lowe の ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        return good

    except Exception as e:
        logger.error(f"FLANN matching failed: {e}")
        return None
