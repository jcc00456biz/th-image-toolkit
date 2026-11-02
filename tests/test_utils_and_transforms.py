from pathlib import Path

import pytest
from PIL import Image, ImageDraw

from th_image_toolkit.transforms import smart_trim_image
from th_image_toolkit.utils import SortKey, SortOrder, list_files, to_safe_win


def test_to_safe_win_replaces_windows_unsafe_characters() -> None:
    assert to_safe_win("a b/c?.png") == "a_b／c？．png"


def test_list_files_filters_recurses_and_sorts(tmp_path: Path) -> None:
    (tmp_path / "b.PNG").touch()
    (tmp_path / "a.jpg").touch()
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.webp").touch()
    (tmp_path / "ignored.txt").touch()

    assert [path.name for path in list_files(tmp_path, recursive=False)] == [
        "a.jpg",
        "b.PNG",
    ]
    assert [path.name for path in list_files(tmp_path)] == [
        "a.jpg",
        "b.PNG",
        "c.webp",
    ]
    assert [
        path.name
        for path in list_files(
            tmp_path, sort_key=SortKey.NAME, sort_order=SortOrder.DESC
        )
    ] == ["c.webp", "b.PNG", "a.jpg"]


def test_list_files_validates_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        list_files(tmp_path / "missing")

    file_path = tmp_path / "file"
    file_path.touch()
    with pytest.raises(NotADirectoryError):
        list_files(file_path)


def test_smart_trim_removes_empty_border() -> None:
    image = Image.new("RGB", (80, 80), "white")
    ImageDraw.Draw(image).rectangle((15, 20, 60, 55), fill="blue")

    trimmed = smart_trim_image(image, margin_size=8)

    assert trimmed.size == (46, 36)


def test_smart_trim_keeps_image_too_small_to_sample() -> None:
    image = Image.new("RGB", (12, 12), "white")

    assert smart_trim_image(image, margin_size=8) is image


def test_smart_trim_keeps_uniform_image_and_ignores_invalid_margin() -> None:
    image = Image.new("RGB", (80, 80), "white")

    assert smart_trim_image(image, margin_size=8) is image
    assert smart_trim_image(image, margin_size=0) is image
