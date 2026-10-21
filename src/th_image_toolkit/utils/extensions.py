#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ImageMagick が扱える拡張子の定義モジュール。
他の処理（validator, ops, GUI, CLI）から参照される。
"""

# 一般的なラスター画像
RASTER_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
    ".avif",
    ".heic",
    ".heif",
}

# RAW画像（必要なら使う）
RAW_EXTENSIONS = {
    ".cr2",
    ".cr3",
    ".nef",
    ".arw",
    ".dng",
    ".orf",
    ".rw2",
}

# ベクター画像
VECTOR_EXTENSIONS = {
    ".svg",
    ".pdf",
    ".eps",
    ".ps",
}

# ImageMagick が扱える拡張子の統合セット
SUPPORTED_EXTENSIONS = RASTER_EXTENSIONS | RAW_EXTENSIONS | VECTOR_EXTENSIONS
