#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import subprocess
from pathlib import Path
from subprocess import CompletedProcess

logger = logging.getLogger(__name__)


class MagickExecutionError(Exception):
    """Raised when ImageMagick execution fails."""


class MagickNotFoundError(Exception):
    """Raised when the bundled ImageMagick is missing."""


class TesseractExecutionError(Exception):
    """Raised when Tesseract OCR execution fails."""


class TesseractNotFoundError(Exception):
    """Raised when the bundled Tesseract OCR is missing."""


def _resolve_magick_path() -> Path:
    """Dynamically resolve the path to the bundled magick.exe.

    Returns:
        Path to the bundled executable.

    Raises:
        MagickNotFoundError: If no bundled executable is found.
    """
    current = Path(__file__).resolve().parent

    # Walk up the parent directories to find bin/ImageMagick/magick.exe
    while current != current.parent:
        # 1. Check for bin/ImageMagick at the current level
        exe_path = current / "bin" / "ImageMagick" / "magick.exe"
        if exe_path.exists():
            logger.info(f"Using bundled ImageMagick: {exe_path}")
            return exe_path

        # 2. Check for image_processing/bin/ImageMagick
        alt_path = (
            current / "image_processing" / "bin" / "ImageMagick" / "magick.exe"
        )
        if alt_path.exists():
            logger.info(f"Using bundled ImageMagick: {alt_path}")
            return alt_path

        # 3. Check for th_image_toolkit/bin/ImageMagick
        th_path = (
            current / "th_image_toolkit" / "bin" / "ImageMagick" / "magick.exe"
        )
        if th_path.exists():
            logger.info(f"Using bundled ImageMagick: {th_path}")
            return th_path

        current = current.parent

    # Raise an error if no bundled executable was found
    base_dir = Path(__file__).resolve().parent / "bin" / "ImageMagick"
    logger.error(
        f"ImageMagick directory or magick.exe missing near: {base_dir}"
    )
    raise MagickNotFoundError(
        f"ImageMagick (magick.exe) not found in bundled paths.: {base_dir}"
    )


def _resolve_tesseract_path() -> Path:
    """Dynamically resolve the path to the bundled tesseract.exe.

    Returns:
        Path to the bundled executable.

    Raises:
        TesseractNotFoundError: If no bundled executable is found.
    """
    current = Path(__file__).resolve().parent

    while current != current.parent:
        # 1. Check for bin/Tesseract-OCR at the current level
        exe_path = current / "bin" / "Tesseract-OCR" / "tesseract.exe"
        if exe_path.exists():
            logger.info(f"Using bundled Tesseract: {exe_path}")
            return exe_path

        # 2. Check for th_image_toolkit/bin/Tesseract-OCR
        th_path = (
            current
            / "th_image_toolkit"
            / "bin"
            / "Tesseract-OCR"
            / "tesseract.exe"
        )
        if th_path.exists():
            logger.info(f"Using bundled Tesseract: {th_path}")
            return th_path

        # 3. Check for image_processing/bin/Tesseract-OCR
        alt_path = (
            current
            / "image_processing"
            / "bin"
            / "Tesseract-OCR"
            / "tesseract.exe"
        )
        if alt_path.exists():
            logger.info(f"Using bundled Tesseract: {alt_path}")
            return alt_path

        current = current.parent

    base_dir = Path(__file__).resolve().parent / "bin" / "Tesseract-OCR"
    logger.error(
        f"Tesseract directory or tesseract.exe missing near: {base_dir}"
    )
    raise TesseractNotFoundError(
        f"Tesseract (tesseract.exe) not found in bundled paths.: {base_dir}"
    )


def run_magick(
    args: list[str], *, timeout: int | None = None
) -> CompletedProcess[str]:
    """Run the bundled ImageMagick executable.

    Args:
        args: Arguments passed to ImageMagick.
        timeout: Optional timeout in seconds.

    Returns:
        The completed process result.

    Raises:
        MagickNotFoundError: If the bundled executable is missing.
        MagickExecutionError: If execution times out or
        returns a non-zero code.
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


def run_tesseract(
    args: list[str], *, timeout: int | None = None
) -> CompletedProcess[str]:
    """Execute Tesseract OCR using the bundled portable version.

    Args:
        args: Arguments passed to Tesseract.
        timeout: Optional timeout in seconds.

    Returns:
        The completed process result.

    Raises:
        TesseractNotFoundError: If the bundled executable is missing.
        TesseractExecutionError: If execution times out or
        returns a non-zero code.
    """
    tesseract = _resolve_tesseract_path()
    tessdata_dir = tesseract.parent / "tessdata"

    # Add --tessdata-dir automatically if it is not already in the arguments
    cmd = [str(tesseract)]
    if "--tessdata-dir" not in args:
        cmd.extend(["--tessdata-dir", str(tessdata_dir)])
    cmd.extend(args)

    logger.info(f"Executing Tesseract command: {cmd}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        logger.error(f"Tesseract command timed out: {cmd}")
        raise TesseractExecutionError("Tesseract execution timed out")

    logger.debug(f"Return code: {result.returncode}")
    logger.debug(f"STDOUT: {result.stdout}")
    logger.debug(f"STDERR: {result.stderr}")

    if result.returncode != 0:
        logger.error(
            f"Tesseract failed (code {result.returncode}): {result.stderr}"
        )
        raise TesseractExecutionError(
            f"Tesseract execution failed (code {result.returncode}):\n"
            f"{result.stderr}"
        )

    logger.info("Tesseract execution completed successfully")
    return result
