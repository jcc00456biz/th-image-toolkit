#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path


def to_safe_win(text: str) -> str:
    """Replace unsafe characters with Windows-safe equivalents.

    Args:
        text: Filename text to sanitize.

    Returns:
        Sanitized text.
    """
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
    """Sanitize a filename and add a numeric suffix if it already exists.

    Args:
        target: Desired output path.

    Returns:
        A sanitized path that does not currently exist.
    """

    parent = target.parent

    # Normalize the extension.
    suffix = target.suffix.lower()

    # Sanitize the filename stem.
    safe_stem = to_safe_win(target.stem)

    normalized = parent / f"{safe_stem}{suffix}"

    # Return the path if it is unused.
    if not normalized.exists():
        return normalized

    # Find an unused numbered path.
    index = 1
    while True:
        candidate = parent / f"{safe_stem}({index}){suffix}"
        if not candidate.exists():
            return candidate
        index += 1
