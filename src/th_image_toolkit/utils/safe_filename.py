#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path


def to_safe_win(text: str) -> str:
    """Windows禁止記号および感嘆符を全角化します（括弧は処理しません）。"""
    double_excl = chr(0x203C)
    var_selector = chr(0xFE0E)

    translation_table: dict[str | int, str] = {
        "　": "_",
        " ": "_",
        ".": "．",
        "\\": "￥",
        "/": "／",
        ":": "：",
        ";": "；",
        ",": "，",
        "*": "＊",
        "?": "？",
        '"': "”",
        "<": "＜",
        ">": "＞",
        "|": "｜",
        "!": "！",
        "&": "＆",
        "%": "％",
        "+": "＋",
        "=": "＝",
        "♡": "",
        "♥": "",
        0x203C: "！！",
        0x2048: "？！",
        0x2049: "！？",
    }

    translation = str.maketrans(translation_table)
    text = text.replace(f"{double_excl}{var_selector}", "！！")
    return text.translate(translation)


def generate_safe_filename(target: Path) -> Path:
    """
    Windows 禁止文字を全角化し、拡張子を小文字化し、
    さらに衝突する場合は Windows のように (1), (2)... を付与して
    衝突しないファイル名を返す。
    """

    parent = target.parent

    # 拡張子を小文字化
    suffix = target.suffix.lower()

    # stem に Windows 禁止文字の安全化を適用
    safe_stem = to_safe_win(target.stem)

    normalized = parent / f"{safe_stem}{suffix}"

    # 衝突なしならそのまま返す
    if not normalized.exists():
        return normalized

    # 衝突回避ループ
    index = 1
    while True:
        candidate = parent / f"{safe_stem}({index}){suffix}"
        if not candidate.exists():
            return candidate
        index += 1
