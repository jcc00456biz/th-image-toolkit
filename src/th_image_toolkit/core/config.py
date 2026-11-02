#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import StrEnum


class OutputFormat(StrEnum):
    JPEG = "jpeg"
    PNG = "png"


# Common parameters (always applied when resizing or converting)
# fmt: off
IM_COMMON_PARAMS: list[str] = [
    "-strip",                   # Remove metadata
    "-colorspace",  "sRGB",     # Standardize the color space
    "-filter",      "Lanczos",  # High-quality resizing
    "-density",     "96",       # Standard DPI for Windows/Linux
]

# Parameters always applied when outputting JPEG
IM_JPEG_PARAMS: list[str] = [
    "-quality",     "100",                          # 100% quality
    "-define",      "jpeg:optimize-coding=true",    # Optimized Huffman coding
    "-define",      "jpeg:dct-method=float",        # High-precision DCT
    "-interlace",   "none",                         # Baseline encoding
]

# Parameters always applied when outputting PNG (for archival use)
IM_PNG_PARAMS: list[str] = [
    "-define",  "png:compression-level=9",      # Maximum compression
    "-define",  "png:compression-filter=5",     # Optimal filter
]

# Default unsharp mask parameters
IM_UNSHARP_PARAMS: list[str] = [
    "-unsharp", "12x6+0.5+0",
]
# fmt: on
