import platform
import sys

from setuptools import Distribution, setup
from wheel.bdist_wheel import bdist_wheel


class WindowsBinaryDistribution(Distribution):
    def has_ext_modules(self) -> bool:
        return True


class WindowsWheelCommand(bdist_wheel):
    def get_tag(self) -> tuple[str, str, str]:
        return "py3", "none", "win_amd64"


if sys.platform != "win32" or platform.machine().lower() not in {
    "amd64",
    "x86_64",
}:
    raise RuntimeError(
        "th-image-toolkit wheels can only be built on 64-bit x86 Windows."
    )

setup(
    distclass=WindowsBinaryDistribution,
    cmdclass={"bdist_wheel": WindowsWheelCommand},
)
