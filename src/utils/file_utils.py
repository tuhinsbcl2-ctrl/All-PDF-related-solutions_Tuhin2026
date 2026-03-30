"""
File utility helpers.
"""

import os
import shutil
from pathlib import Path


def get_file_size(path: str) -> int:
    """Return file size in bytes."""
    return os.path.getsize(path)


def get_file_size_str(path: str) -> str:
    """Return human-readable file size."""
    size = get_file_size(path)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def ensure_dir(directory: str) -> None:
    """Create directory if it doesn't exist."""
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_output_path(input_path: str, suffix: str, extension: str) -> str:
    """
    Generate an output file path based on input path.
    e.g. input_path='file.pdf', suffix='_compressed', extension='.pdf'
    -> 'file_compressed.pdf'
    """
    base = Path(input_path)
    return str(base.parent / (base.stem + suffix + extension))


def validate_file_exists(path: str) -> bool:
    """Check that a file exists and is a regular file."""
    return os.path.isfile(path)


def validate_extension(path: str, *extensions: str) -> bool:
    """Check that file has one of the given extensions (case-insensitive)."""
    ext = Path(path).suffix.lower()
    return ext in [e.lower() for e in extensions]


def copy_file(src: str, dst: str) -> None:
    """Copy a file from src to dst."""
    shutil.copy2(src, dst)
