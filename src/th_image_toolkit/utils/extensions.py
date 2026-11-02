#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""File extensions supported by ImageMagick and used across the package."""

# Common raster formats.
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

# Camera RAW formats.
RAW_EXTENSIONS = {
    ".cr2",
    ".cr3",
    ".nef",
    ".arw",
    ".dng",
    ".orf",
    ".rw2",
}

# Vector formats.
VECTOR_EXTENSIONS = {
    ".svg",
    ".pdf",
    ".eps",
    ".ps",
}

# All supported extensions.
SUPPORTED_EXTENSIONS = RASTER_EXTENSIONS | RAW_EXTENSIONS | VECTOR_EXTENSIONS
