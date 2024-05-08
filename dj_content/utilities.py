"""Utilities for the dj_content app."""

from pathlib import Path
from typing import Optional


def read_file_into_array(file_path, encoding: Optional[str] = "utf-8") -> list[str]:
    """Read a file into an array of lines.

    Note: Should move to a "core" or "utilities" app if to be used in multiple apps.

    >>> from dj_content.utilities import read_file_into_array
    >>> file_path = Path("path/to/file.txt")
    >>> lines = read_file_into_array(file_path)
    """
    file_path = Path(file_path)
    file_contents = file_path.read_text(encoding=encoding)
    lines = file_contents.split("\n")

    return lines
