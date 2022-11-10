import importlib
import io
import mimetypes
import re
from urllib.request import urlopen


def open_read_file(path):
    """
    Return a file object from the path. Automatically detects and supports
    URLs and compression. If path is pathlike, it's converted to a string.
    If path is not a string nor pathlike, it's passed through without
    modification.
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
            encoding = response.headers.get_content_charset(failobj="utf-8")
            text = content.decode(encoding)
            return io.StringIO(text)
        else:
            compressed_bytes = io.BytesIO(content)
            return opener(compressed_bytes, "rt")

    # Read from file
    return opener(path, "rt")


encoding_to_module = {
    "gzip": "gzip",
    "bzip2": "bz2",
    "xz": "lzma",
}


def get_opener(filename):
    """
    Automatically detect compression and return the file opening function.
    """
    type_, encoding = mimetypes.guess_type(filename)
    if encoding is None:
        opener = io.open
    else:
        module = encoding_to_module[encoding]
        opener = importlib.import_module(module).open
    return opener
