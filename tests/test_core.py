from pathlib import Path
from subprocess import CompletedProcess, TimeoutExpired

import pytest

from th_image_toolkit.core import (
    ImageOrientation,
    MagickExecutionError,
    MagickNotFoundError,
    TesseractExecutionError,
    run_magick,
    run_tesseract,
)
from th_image_toolkit.core import aspect_ratio, runner


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        ((8, 12), ImageOrientation.PORTRAIT),
        ((12, 8), ImageOrientation.LANDSCAPE),
        ((8, 8), ImageOrientation.SQUARE),
    ],
)
def test_get_image_orientation(image_factory, size, expected) -> None:
    image_path = image_factory(size=size)

    assert aspect_ratio.get_image_orientation(image_path) is expected


def test_get_image_orientation_rejects_missing_image(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        aspect_ratio.get_image_orientation(tmp_path / "missing.png")


def test_run_magick_uses_bundled_executable() -> None:
    result = run_magick(["-version"])

    assert result.returncode == 0
    assert "ImageMagick" in result.stdout


def test_run_magick_raises_when_executable_is_missing(monkeypatch) -> None:
    def missing_executable() -> Path:
        raise MagickNotFoundError("missing")

    monkeypatch.setattr(runner, "_resolve_magick_path", missing_executable)

    with pytest.raises(MagickNotFoundError, match="missing"):
        run_magick(["-version"])


@pytest.mark.parametrize(
    ("result", "raised"),
    [
        (CompletedProcess([], 2, "", "error"), MagickExecutionError),
        (TimeoutExpired(["magick.exe"], 1), MagickExecutionError),
    ],
)
def test_run_magick_reports_execution_failures(
    monkeypatch, tmp_path: Path, result, raised
) -> None:
    monkeypatch.setattr(runner, "_resolve_magick_path", lambda: tmp_path / "magick.exe")

    def fail(*args, **kwargs):
        assert args[0][0] == str(tmp_path / "magick.exe")
        assert kwargs["capture_output"]
        if isinstance(result, BaseException):
            raise result
        return result

    monkeypatch.setattr(runner.subprocess, "run", fail)

    with pytest.raises(raised):
        run_magick(["-version"])


def test_run_tesseract_adds_bundled_tessdata_path(
    monkeypatch, tmp_path: Path
) -> None:
    executable = tmp_path / "Tesseract-OCR" / "tesseract.exe"
    calls = []
    monkeypatch.setattr(runner, "_resolve_tesseract_path", lambda: executable)

    def run(command, **kwargs):
        assert kwargs["capture_output"]
        calls.append(command)
        return CompletedProcess(command, 0, "ok", "")

    monkeypatch.setattr(
        runner.subprocess,
        "run",
        run,
    )

    result = run_tesseract(["input.png", "stdout"])

    assert result.stdout == "ok"
    assert calls[0][:3] == [
        str(executable),
        "--tessdata-dir",
        str(executable.parent / "tessdata"),
    ]


def test_run_tesseract_reports_timeout(monkeypatch, tmp_path: Path) -> None:
    executable = tmp_path / "tesseract.exe"
    monkeypatch.setattr(runner, "_resolve_tesseract_path", lambda: executable)

    def timeout(command, **kwargs):
        assert kwargs["capture_output"]
        raise TimeoutExpired(command, 1)

    monkeypatch.setattr(runner.subprocess, "run", timeout)

    with pytest.raises(TesseractExecutionError):
        run_tesseract(["input.png", "stdout"])
