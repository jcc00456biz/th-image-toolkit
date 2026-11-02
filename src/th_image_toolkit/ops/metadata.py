#!/usr/init/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from pathlib import Path

from PIL import ExifTags, Image
from PIL.PngImagePlugin import PngInfo

# Internal mappings from common fields to format-specific tags.
_JPEG_TAG_MAP = {
    "title": "ImageDescription",
    "maker": "Artist",
    "label": "Copyright",
    "series": "XPTitle",
    "release_date": "DateTimeOriginal",
    "product_code": "XPComment",
    "user_define": "XPAuthor",
}

_PNG_TAG_MAP = {
    "title": "Title",
    "maker": "Maker",
    "label": "Label",
    "series": "Series",
    "release_date": "ReleaseDate",
    "product_code": "ProductCode",
    "user_define": "UserDefine",
}


@dataclass(slots=True)
class ImageMetadata:
    """Common image metadata independent of file format."""

    title: str = ""
    maker: str = ""
    label: str = ""
    series: str = ""
    release_date: str = ""
    product_code: str = ""
    user_define: str = ""

    def to_jpeg_dict(self) -> dict[str, str]:
        """Map common metadata fields to JPEG tag names.

        Returns:
            Metadata keyed by JPEG tag names.
        """
        result: dict[str, str] = {}
        for field_name, jpeg_tag_name in _JPEG_TAG_MAP.items():
            val = getattr(self, field_name, "")
            if val:
                result[jpeg_tag_name] = str(val)
        return result

    @classmethod
    def from_jpeg_dict(cls, raw_tags: dict[str, str]) -> "ImageMetadata":
        """Create metadata from a dictionary of JPEG tags.

        Args:
            raw_tags: Metadata keyed by JPEG tag names.

        Returns:
            Parsed image metadata.
        """
        extracted_data: dict[str, str] = {}
        reverse_map = {v: k for k, v in _JPEG_TAG_MAP.items()}

        for tag_key, value in raw_tags.items():
            field_name = reverse_map.get(str(tag_key))
            if field_name and value:
                val_str = str(value).strip()
                if val_str:
                    extracted_data[field_name] = val_str

        return cls(**extracted_data)

    def to_png_dict(self) -> dict[str, str]:
        """Map common metadata fields to PNG text keys.

        Returns:
            Metadata keyed by PNG text names.
        """
        result: dict[str, str] = {}
        for field_name, png_key in _PNG_TAG_MAP.items():
            val = getattr(self, field_name, "")
            if val:
                result[png_key] = str(val)
        return result

    @classmethod
    def from_png_dict(cls, raw_tags: dict[str, str]) -> "ImageMetadata":
        """Create metadata from a dictionary of PNG text keys.

        Args:
            raw_tags: Metadata keyed by PNG text names.

        Returns:
            Parsed image metadata.
        """
        extracted_data: dict[str, str] = {}
        reverse_map = {v: k for k, v in _PNG_TAG_MAP.items()}

        for key, value in raw_tags.items():
            field_name = reverse_map.get(str(key))
            if field_name and value:
                val_str = str(value).strip()
                if val_str:
                    extracted_data[field_name] = val_str

        return cls(**extracted_data)


def get_image_metadata(image_path: str | Path) -> ImageMetadata:
    """Extract metadata from an image into a common object.

    Args:
        image_path: Path to the image file.

    Returns:
        Extracted metadata, or empty metadata if no supported tags are found.

    Raises:
        OSError: If the image cannot be opened.
    """
    path = Path(image_path)

    with Image.open(path) as img:
        file_ext = path.suffix.lower()

        if file_ext in [".jpg", ".jpeg"]:
            exif_data = img.getexif()
            if exif_data:
                raw_tags = {
                    str(ExifTags.TAGS.get(tid, tid)): (
                        val.decode("utf-8", errors="ignore")
                        if isinstance(val, bytes)
                        else str(val)
                    )
                    for tid, val in exif_data.items()
                    if val
                }
                return ImageMetadata.from_jpeg_dict(raw_tags)

        elif file_ext == ".png":
            if img.info:
                raw_tags = {
                    str(k): (
                        v.decode("utf-8", errors="ignore")
                        if isinstance(v, bytes)
                        else str(v)
                    )
                    for k, v in img.info.items()
                    if v
                }
                return ImageMetadata.from_png_dict(raw_tags)

    return ImageMetadata()


def set_image_metadata(
    image_path: str | Path,
    metadata: ImageMetadata,
    output_path: str | Path | None = None,
) -> Path:
    """Write common metadata to an image and save it.

    Args:
        image_path: Path to the source image.
        metadata: Metadata to write.
        output_path: Optional destination path; defaults to image_path.

    Returns:
        Path to the saved image.

    Raises:
        OSError: If the image cannot be read or saved.
    """
    path = Path(image_path)
    dest_path = Path(output_path) if output_path else path

    with Image.open(path) as img:
        file_ext = path.suffix.lower()

        if file_ext in [".jpg", ".jpeg"]:
            exif = img.getexif()
            reverse_exif_tags = {v: k for k, v in ExifTags.TAGS.items()}
            jpeg_tags = metadata.to_jpeg_dict()

            for jpeg_tag_name, val in jpeg_tags.items():
                if jpeg_tag_name in reverse_exif_tags:
                    tag_id = reverse_exif_tags[jpeg_tag_name]
                    exif[tag_id] = val

            img.save(dest_path, exif=exif)

        elif file_ext == ".png":
            pnginfo = PngInfo()
            current_info = img.info if img.info else {}

            for k, v in current_info.items():
                if isinstance(v, (str, bytes)):
                    val_str = (
                        v.decode("utf-8", errors="ignore")
                        if isinstance(v, bytes)
                        else v
                    )
                    pnginfo.add_text(str(k), val_str)

            png_tags = metadata.to_png_dict()
            for png_key, val in png_tags.items():
                pnginfo.add_text(png_key, str(val))

            img.save(dest_path, pnginfo=pnginfo)

        else:
            img.save(dest_path)

    return dest_path


def strip_image_metadata(
    image_path: str | Path,
    output_path: str | Path | None = None,
) -> Path:
    """Remove all metadata from an image and save it.

    Args:
        image_path: Path to the source image.
        output_path: Optional destination path; defaults to image_path.

    Returns:
        Path to the saved image.

    Raises:
        OSError: If the image cannot be read or saved.
    """
    path = Path(image_path)
    dest_path = Path(output_path) if output_path else path

    with Image.open(path) as img:
        img.save(dest_path)

    return dest_path


def overwrite_image_metadata(
    image_path: str | Path,
    metadata: ImageMetadata,
    output_path: str | Path | None = None,
) -> Path:
    """Replace existing metadata with the supplied metadata.

    Args:
        image_path: Path to the source image.
        metadata: Metadata to write after removing existing metadata.
        output_path: Optional destination path; defaults to image_path.

    Returns:
        Path to the saved image.

    Raises:
        OSError: If the image cannot be read or saved.
    """
    path = Path(image_path)
    dest_path = Path(output_path) if output_path else path

    strip_image_metadata(path, dest_path)
    set_image_metadata(dest_path, metadata, dest_path)

    return dest_path
