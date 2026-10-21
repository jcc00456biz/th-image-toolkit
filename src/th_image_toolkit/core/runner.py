#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import List, Optional

logger = logging.getLogger(__name__)


class MagickExecutionError(Exception):
    """Raised when ImageMagick execution fails."""


class MagickNotFoundError(Exception):
    """Raised when the bundled ImageMagick is missing."""


def _resolve_magick_path() -> Path:
    """
    バンドルされた magick.exe のパスを動的に解決する。
    スクリプトの位置から上位ディレクトリを遡り、image_processing/bin/ImageMagick/magick.exe を確実に検出する。
    """
    current = Path(__file__).resolve().parent

    # 親ディレクトリを順に遡って bin/ImageMagick/magick.exe を探す
    while current != current.parent:
        # 1. 現在の階層に bin/ImageMagick がある場合
        exe_path = current / "bin" / "ImageMagick" / "magick.exe"
        if exe_path.exists():
            logger.info(f"Using bundled ImageMagick: {exe_path}")
            return exe_path

        # 2. image_processing/bin/ImageMagick として見つかる場合
        alt_path = (
            current / "image_processing" / "bin" / "ImageMagick" / "magick.exe"
        )
        if alt_path.exists():
            logger.info(f"Using bundled ImageMagick: {alt_path}")
            return alt_path

        current = current.parent

    # 見つからなかった場合はエラーを投げる
    base_dir = Path(__file__).resolve().parent / "bin" / "ImageMagick"
    logger.error(
        f"ImageMagick directory or magick.exe missing near: {base_dir}"
    )
    raise MagickNotFoundError(
        f"ImageMagick (magick.exe) not found in bundled paths.: {base_dir}"
    )


def run_magick(
    args: List[str], *, timeout: Optional[int] = None
) -> CompletedProcess[str]:
    """
    Execute ImageMagick using the bundled portable version.

    Parameters
    ----------
    args : List[str]
        Command arguments (e.g. ["convert", "in.jpg", "-resize", "50%",
        "out.jpg"])
    timeout : Optional[int]
        Optional timeout for subprocess execution.

    Returns
    -------
    subprocess.CompletedProcess
        Contains stdout, stderr, and returncode.

    Raises
    ------
    MagickNotFoundError
        If the bundled ImageMagick is missing.
    MagickExecutionError
        If ImageMagick returns a non-zero exit code.
    """
    magick = _resolve_magick_path()

    cmd = [str(magick)] + args
    logger.info(f"Executing ImageMagick command: {cmd}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        logger.error(f"ImageMagick command timed out: {cmd}")
        raise MagickExecutionError("ImageMagick execution timed out")

    logger.debug(f"Return code: {result.returncode}")
    logger.debug(f"STDOUT: {result.stdout}")
    logger.debug(f"STDERR: {result.stderr}")

    if result.returncode != 0:
        logger.error(
            f"ImageMagick failed (code {result.returncode}): {result.stderr}"
        )
        raise MagickExecutionError(
            f"ImageMagick execution failed (code {result.returncode}):\n"
            f"{result.stderr}"
        )

    logger.info("ImageMagick execution completed successfully")
    return result
