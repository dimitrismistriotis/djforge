"""Utilities for the dj_content app."""

from pathlib import Path


def read_file_into_array(file_path) -> list[str]:
    """Read a file into an array of lines.

    Note: Should move to a "core" or "utilities" app if to be used in multiple apps.

    >>> from dj_content.utilities import read_file_into_array
    >>> file_path = Path("path/to/file.txt")
    >>> lines = read_file_into_array(file_path)
    """
    file_path = Path(file_path)
    file_contents = file_path.read_text()
    lines = file_contents.split("\n")

    return lines
