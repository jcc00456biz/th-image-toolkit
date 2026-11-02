# th-image-toolkit

Python toolkit for image conversion, cropping, resizing, metadata, analysis,
smart trimming, and feature matching. ImageMagick is bundled with the package;
Pillow and OpenCV are used for in-process image operations.

## Platform and Python

This package is published for **64-bit Windows (x86-64)** only because its
bundled ImageMagick executable is a Windows x64 binary. Python 3.11 or later is
required.

## Installation

```powershell
py -m pip install th-image-toolkit
```

## Quick start

```python
from pathlib import Path

from th_image_toolkit.core import IMAGE_SCALE_PIXELS, ImageScale, OutputFormat
from th_image_toolkit.metrics import get_image_resolution
from th_image_toolkit.ops import convert_image_format

source = Path("input.png")
destination = Path("output.jpg")

print(IMAGE_SCALE_PIXELS[ImageScale.CD_JACKET])
print(get_image_resolution(source))
convert_image_format(source, destination, OutputFormat.JPEG)
```

The public modules are `core`, `metrics`, `ops`, `signatures`, `matching`,
`transforms`, and `utils`. Their exported functions and classes are listed in
each module's `__all__`.

## Development

```powershell
py -m pip install -e ".[test]"
py -m pytest
py -m build
```

The wheel is tagged `py3-none-win_amd64` and contains the bundled
`ImageMagick` directory.
