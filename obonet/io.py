from __future__ import annotations

import importlib
import io
import logging
import mimetypes
import re
from urllib.request import urlopen


def open_read_file(path, encoding: str | None = None):
    """
    Return a file object from the path. Automatically detects and supports
    URLs and compression. If path is pathlike, it's converted to a string.
    If path is not a string nor pathlike, it's passed through without
    modification. Use encoding to set the text character set encoding.
    Use `encoding=None` to use the platform-dependent default locale encoding.
    """
    # Convert pathlike objects to string paths
    if hasattr(path, "__fspath__"):
        path = path.__fspath__()

    if not isinstance(path, str):
        # Passthrough open file buffers without modification
        return path

    # Get opener based on file extension
    opener = get_opener(path)

    # Read from URL
    if re.match("^(http|ftp)s?://", path):
        with urlopen(path) as response:
            content = response.read()
        if opener == io.open:
            if not encoding:
                encoding = response.headers.get_content_charset(failobj="utf-8")
            logging.info(f"Will decode content from {path} using {encoding} charset.")
            text = content.decode(encoding)
            return io.StringIO(text)
        else:
            compressed_bytes = io.BytesIO(content)
            return opener(compressed_bytes, "rt", encoding=encoding)

    # Read from file
    return opener(path, "rt", encoding=encoding)


compression_to_module = {
    "gzip": "gzip",
    "bzip2": "bz2",
    "xz": "lzma",
}


def get_opener(filename):
    """
    Automatically detect compression and return the file opening function.
    """
    _type, compression = mimetypes.guess_type(filename)
    if compression is None:
        opener = io.open
    else:
        module = compression_to_module[compression]
        opener = importlib.import_module(module).open
    return opener
