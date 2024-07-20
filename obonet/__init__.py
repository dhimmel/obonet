from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .read import read_obo

__all__ = [
    "read_obo",
]


def _get_version() -> str | None:
    try:
        version_ = version("obonet")
        # encountered mypy error [no-any-return] on Python 3.11
        assert isinstance(version_, str)
        return version_
    except PackageNotFoundError:
        return None


__version__ = _get_version()
