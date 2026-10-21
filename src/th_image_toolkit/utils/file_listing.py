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
    return p.name.lower()


def _sort_by_mtime(p: Path) -> str:
    # float → str に統一して型を揃える
    return str(p.stat().st_mtime)


def list_files(
    root: Path,
    recursive: bool = True,
    sort_key: SortKey = SortKey.NAME,
    sort_order: SortOrder = SortOrder.ASC,
) -> list[Path]:
    """
    指定ディレクトリ以下のサポートされている画像ファイル一覧を取得する。
    デフォルトではサブディレクトリも対象にする。
    ソートはファイル名 or 更新日時で昇順/降順を指定可能。
    デフォルトはファイル名昇順。
    """

    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    # ファイル一覧取得（ImageMagick サポート拡張子に絞り込む）
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

    # ソートキー選択（lambda 不使用）
    if sort_key is SortKey.NAME:
        key_func = _sort_by_name
    else:
        key_func = _sort_by_mtime

    reverse = sort_order is SortOrder.DESC

    return sorted(file_list, key=key_func, reverse=reverse)
