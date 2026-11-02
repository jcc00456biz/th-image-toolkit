from collections.abc import Callable
from pathlib import Path

import pytest
from PIL import Image


@pytest.fixture
def image_factory(
    tmp_path: Path,
) -> Callable[..., Path]:
    def create_image(
        name: str = "image.png",
        size: tuple[int, int] = (32, 24),
        color: tuple[int, int, int] = (40, 80, 120),
    ) -> Path:
        path = tmp_path / name
        Image.new("RGB", size, color).save(path)
        return path

    return create_image
