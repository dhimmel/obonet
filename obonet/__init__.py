from .read import read_obo

__all__ = [
    "read_obo",
]


def _get_version():
    # https://github.com/pypa/setuptools_scm#retrieving-package-version-at-runtime
    from pkg_resources import DistributionNotFound, get_distribution

    try:
        return get_distribution("obonet").version
    except DistributionNotFound:
        return None


__version__ = _get_version()
