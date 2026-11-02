#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import StrEnum
from pathlib import Path
from typing import Iterable, final

from .extensions import SUPPORTED_EXTENSIONS


@final
class SortKey(StrEnum):
    NAME = "name"
    MTIME = "mtime"


@final
class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


def _sort_by_name(p: Path) -> str:
    """Return a lowercase filename sort key.

    Args:
        p: File path to sort.

    Returns:
        Lowercase filename.
    """
    return p.name.lower()


def _sort_by_mtime(p: Path) -> str:
    # Return a string to keep the sort key type consistent.
    """Return a file's modification time as a string sort key.

    Args:
        p: File path to sort.

    Returns:
        Modification time as a string.
    """
    return str(p.stat().st_mtime)


def list_files(
    root: Path,
    recursive: bool = True,
    sort_key: SortKey = SortKey.NAME,
    sort_order: SortOrder = SortOrder.ASC,
) -> list[Path]:
    """List supported images, optionally including subdirectories.

    Sort by name or modification time in ascending or descending order.

    Args:
        root: Directory to search.
        recursive: Whether to include nested directories.
        sort_key: Field used to sort the results.
        sort_order: Sort direction.

    Returns:
        Supported image paths in the requested order.

    Raises:
        FileNotFoundError: If root does not exist.
        NotADirectoryError: If root is not a directory.
    """

    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    # Collect files with supported ImageMagick extensions.
    if recursive:
        files: Iterable[Path] = (
            p
            for p in root.rglob("*")
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
        )
    else:
        files = (
            p
            for p in root.iterdir()
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
        )

    file_list = list(files)

    # Select the sort key.
    if sort_key is SortKey.NAME:
        key_func = _sort_by_name
    else:
        key_func = _sort_by_mtime

    reverse = sort_order is SortOrder.DESC

    return sorted(file_list, key=key_func, reverse=reverse)
