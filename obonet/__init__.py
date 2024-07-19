from __future__ import annotations
import sys

from .read import read_obo

__all__ = [
    "read_obo",
]


def _get_version() -> str | None:
    # https://github.com/pypa/setuptools_scm#retrieving-package-version-at-runtime
    if sys.version_info >= (3, 8):
        from importlib.metadata import PackageNotFoundError, version

        try:
            return version("obonet")
        except PackageNotFoundError:
            return None
    else:
        from pkg_resources import DistributionNotFound, get_distribution

        try:
            return str(get_distribution("obonet").version)
        except DistributionNotFound:
            return None


__version__ = _get_version()
