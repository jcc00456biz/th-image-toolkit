def test_public_package_imports() -> None:
    from th_image_toolkit import (
        core,
        matching,
        metrics,
        ops,
        signatures,
        transforms,
        utils,
    )
    from th_image_toolkit.core import IMAGE_SCALE_PIXELS, ImageScale

    assert core.OutputFormat.PNG.value == "png"
    assert IMAGE_SCALE_PIXELS[ImageScale.CD_JACKET] == (1416, 1416)
    assert callable(metrics.get_image_resolution)
    assert callable(ops.crop_image)
    assert callable(signatures.compute_phash)
    assert callable(matching.match_orb)
    assert callable(transforms.smart_trim_image)
    assert callable(utils.list_files)
    for package in (
        core,
        matching,
        metrics,
        ops,
        signatures,
        transforms,
        utils,
    ):
        assert all(hasattr(package, name) for name in package.__all__)
