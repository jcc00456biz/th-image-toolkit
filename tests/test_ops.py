from pathlib import Path

import pytest
from PIL import Image

from th_image_toolkit.core import OutputFormat
from th_image_toolkit.ops import convert, crop, level, resize


def test_convert_image_format_builds_command(
    monkeypatch, image_factory, tmp_path: Path
) -> None:
    source = image_factory()
    destination = tmp_path / "nested" / "converted.jpg"
    commands = []
    monkeypatch.setattr(convert, "run_magick", lambda args: commands.append(args))

    assert convert.convert_image_format(source, destination, OutputFormat.JPEG)

    assert destination.parent.is_dir()
    assert commands[0][0] == str(source)
    assert commands[0][-1] == str(destination)


def test_convert_image_format_rejects_missing_or_unsupported_source(
    monkeypatch, tmp_path: Path
) -> None:
    def unexpected_call(args) -> None:
        raise AssertionError(f"ImageMagick should not run: {args}")

    monkeypatch.setattr(convert, "run_magick", unexpected_call)
    assert not convert.convert_image_format(
        tmp_path / "missing.png", tmp_path / "out.jpg"
    )

    source = tmp_path / "document.txt"
    source.write_text("not an image", encoding="utf-8")
    assert not convert.convert_image_format(source, tmp_path / "out.jpg")


def test_crop_includes_both_boundary_pixels(image_factory, tmp_path: Path) -> None:
    source = image_factory(size=(8, 6), color=(0, 0, 0))
    with Image.open(source) as image:
        image.putpixel((2, 1), (255, 0, 0))
        image.putpixel((4, 3), (0, 255, 0))
        image.save(source)
    destination = tmp_path / "crop.png"

    result = crop.crop_image(source, crop.CropBox(2, 1, 4, 3), destination)

    assert result == destination
    with Image.open(destination) as cropped:
        assert cropped.size == (3, 3)
        assert cropped.getpixel((0, 0)) == (255, 0, 0)
        assert cropped.getpixel((2, 2)) == (0, 255, 0)


@pytest.mark.parametrize(
    ("orientation", "expected_sizes"),
    [
        (crop.SplitOrientation.VERTICAL, ((3, 4), (3, 4))),
        (crop.SplitOrientation.HORIZONTAL, ((5, 3), (5, 2))),
    ],
)
def test_split_and_crop_image(
    image_factory, tmp_path: Path, orientation, expected_sizes
) -> None:
    source = image_factory(size=(5, 4))
    first, second = crop.split_and_crop_image(
        source,
        crop.CropBox(0, 0, 4, 3),
        crop.SplitParams(2, orientation),
        output_dir=tmp_path / "split",
    )

    with Image.open(first) as first_image, Image.open(second) as second_image:
        assert (first_image.size, second_image.size) == expected_sizes


def test_generated_output_paths_are_safe_and_collision_free(tmp_path: Path) -> None:
    source = tmp_path / "unsafe name.PNG"

    first = crop.generate_cropped_path(source)
    assert first.name == "unsafe_name_crop.png"
    first.touch()
    assert crop.generate_cropped_path(source).name == "unsafe_name_crop(1).png"

    left, right = crop.generate_split_paths(
        source, crop.SplitOrientation.VERTICAL
    )
    assert left.name == "unsafe_name_split_l.png"
    assert right.name == "unsafe_name_split_r.png"


def test_apply_auto_levels_builds_command(
    monkeypatch, image_factory, tmp_path: Path
) -> None:
    source = image_factory()
    destination = tmp_path / "out" / "level.png"
    commands = []
    monkeypatch.setattr(level, "run_magick", lambda args: commands.append(args))

    assert level.apply_auto_levels(source, destination) == destination
    assert destination.parent.is_dir()
    assert "-auto-level" in commands[0]
    assert commands[0][-1] == str(destination)


@pytest.mark.parametrize(
    ("target_size", "auto_level", "should_sharpen"),
    [((16, 12), False, False), ((64, 48), True, True)],
)
def test_resize_and_sharpen_selects_filter_options(
    monkeypatch,
    image_factory,
    tmp_path: Path,
    target_size,
    auto_level,
    should_sharpen,
) -> None:
    source = image_factory(size=(32, 24))
    destination = tmp_path / "resized.png"
    commands = []
    monkeypatch.setattr(resize, "run_magick", lambda args: commands.append(args))

    assert (
        resize.resize_and_sharpen(
            source,
            target_size[0],
            target_size[1],
            destination,
            auto_level=auto_level,
        )
        == destination
    )
    assert "-resize" in commands[0]
    assert ("-auto-level" in commands[0]) is auto_level
    assert ("-unsharp" in commands[0]) is should_sharpen
