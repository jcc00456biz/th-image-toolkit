#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import StrEnum


class OutputFormat(StrEnum):
    JPEG = "jpeg"
    PNG = "png"


# 共通パラメータ（リサイズ・変換時に必ず付与）
# fmt: off
IM_COMMON_PARAMS: list[str] = [
    "-strip",                   # メタデータ削除
    "-colorspace",  "sRGB",     # 色空間統一
    "-filter",      "Lanczos",  # 高品質リサイズ
    "-density",     "96",       # Windows/Linux の標準 DPI
]

# JPEG 出力時に必ず付与するパラメータ
IM_JPEG_PARAMS: list[str] = [
    "-quality",     "100",                          # 量子化率100%
    "-define",      "jpeg:optimize-coding=true",    # 最適化ハフマン
    "-define",      "jpeg:dct-method=float",        # 高精度DCT
    "-interlace",   "none",                         # ベースライン化（非プログレッシブ）
]

# PNG 出力時に必ず付与するパラメータ（アーカイブ用途）
IM_PNG_PARAMS: list[str] = [
    "-define",  "png:compression-level=9",      # 最大圧縮
    "-define",  "png:compression-filter=5",     # 最適フィルタ
]

# アンシャープマスクの標準パラメータ
IM_UNSHARP_PARAMS: list[str] = [
    "-unsharp", "12x6+0.5+0",
]
# fmt: on
