from pathlib import Path

from PIL import Image, ImageDraw

from th_image_toolkit.metrics import (
    compute_color_histogram,
    compute_image_sharpness,
    compute_line_art_sharpness,
    get_image_resolution,
)


def test_get_image_resolution(image_factory) -> None:
    image_path = image_factory(size=(17, 11))

    assert get_image_resolution(image_path) == (17, 11)


def test_metrics_handle_missing_and_invalid_images(tmp_path: Path) -> None:
    missing = tmp_path / "missing.png"
    invalid = tmp_path / "invalid.png"
    invalid.write_bytes(b"not an image")

    assert get_image_resolution(missing) is None
    assert compute_color_histogram(missing) is None
    assert compute_image_sharpness(missing) is None
    assert compute_line_art_sharpness(missing) is None
    assert get_image_resolution(invalid) is None
    assert compute_color_histogram(invalid) is None


def test_compute_color_histogram_counts_rgb_pixels(image_factory) -> None:
    image_path = image_factory(size=(4, 3), color=(10, 20, 30))

    histogram = compute_color_histogram(image_path)

    assert histogram is not None
    assert len(histogram) == 768
    assert histogram[10] == 12
    assert histogram[256 + 20] == 12
    assert histogram[512 + 30] == 12
    assert sum(histogram[:256]) == 12


def test_sharpness_metrics_measure_edges(tmp_path: Path) -> None:
    image_path = tmp_path / "edges.png"
    image = Image.new("L", (64, 64), 255)
    draw = ImageDraw.Draw(image)
    draw.rectangle((8, 8, 55, 55), fill=0)
    image.convert("RGB").save(image_path)

    sharpness = compute_image_sharpness(image_path)
    line_sharpness = compute_line_art_sharpness(image_path)
    assert sharpness is not None and sharpness > 0
    assert line_sharpness is not None and line_sharpness > 0


def test_sharpness_metrics_return_zero_for_flat_image(image_factory) -> None:
    image_path = image_factory(size=(32, 24), color=(128, 128, 128))

    assert compute_image_sharpness(image_path) == 0
    assert compute_line_art_sharpness(image_path) == 0
