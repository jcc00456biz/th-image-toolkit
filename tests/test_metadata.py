from pathlib import Path

from PIL import Image, PngImagePlugin

from th_image_toolkit.ops.metadata import (
    ImageMetadata,
    get_image_metadata,
    overwrite_image_metadata,
    set_image_metadata,
    strip_image_metadata,
)


def test_metadata_dictionary_round_trips() -> None:
    metadata = ImageMetadata(title="A title", maker="A maker", label="Copyright")

    assert ImageMetadata.from_png_dict(metadata.to_png_dict()) == metadata
    assert ImageMetadata.from_jpeg_dict(metadata.to_jpeg_dict()) == metadata
    assert ImageMetadata.from_png_dict({"Unknown": "ignored"}) == ImageMetadata()


def test_png_metadata_set_get_strip_and_overwrite(tmp_path: Path) -> None:
    source = tmp_path / "metadata.png"
    image = Image.new("RGB", (4, 3), (25, 50, 75))
    info = PngImagePlugin.PngInfo()
    info.add_text("Existing", "preserved initially")
    image.save(source, pnginfo=info)

    first = ImageMetadata(title="Initial title", maker="Studio")
    set_image_metadata(source, first)
    assert get_image_metadata(source) == first

    replacement = ImageMetadata(title="Replacement")
    overwrite_image_metadata(source, replacement)
    assert get_image_metadata(source) == replacement

    clean = tmp_path / "clean.png"
    strip_image_metadata(source, clean)
    with Image.open(clean) as stripped:
        assert "Title" not in stripped.info
        assert "Maker" not in stripped.info
