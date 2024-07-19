from __future__ import annotations

from .read import read_obo

__all__ = [
    "read_obo",
]


def _get_version() -> str | None:
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("obonet")
    except PackageNotFoundError:
        return None


__version__ = _get_version()
