from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from th_image_toolkit.matching import match_flann, match_orb
from th_image_toolkit.signatures import (
    compute_akaze,
    compute_orb,
    compute_phash,
    compute_sift,
)


def _save_feature_image(path: Path) -> Path:
    image = Image.new("RGB", (256, 256), "white")
    draw = ImageDraw.Draw(image)
    for x in range(16, 240, 32):
        for y in range(16, 240, 32):
            draw.rectangle((x, y, x + 12, y + 12), fill="black")
            draw.ellipse((x + 14, y + 14, x + 24, y + 24), outline="black", width=2)
    image.save(path)
    return path


def test_compute_phash_is_stable_for_same_image(image_factory) -> None:
    image_path = image_factory()

    first = compute_phash(image_path)

    assert first is not None
    assert len(first) == 16
    assert compute_phash(image_path) == first


def test_feature_detectors_return_descriptors_and_match(tmp_path: Path) -> None:
    image_path = _save_feature_image(tmp_path / "features.png")

    orb_features = compute_orb(image_path)
    sift_features = compute_sift(image_path)
    akaze_features = compute_akaze(image_path)

    assert orb_features is not None and len(orb_features[0]) > 0
    assert sift_features is not None and len(sift_features[0]) > 0
    assert akaze_features is not None and len(akaze_features[0]) > 0
    assert match_orb(orb_features[1], orb_features[1])
    assert match_flann(sift_features[1], sift_features[1])


def test_feature_helpers_handle_missing_input(tmp_path: Path) -> None:
    missing = tmp_path / "missing.png"

    assert compute_phash(missing) is None
    assert compute_orb(missing) is None
    assert compute_sift(missing) is None
    assert compute_akaze(missing) is None
    assert match_orb(None, np.ones((1, 32), dtype=np.uint8)) is None
    assert match_flann(None, np.ones((1, 128), dtype=np.float32)) is None
