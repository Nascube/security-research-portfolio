"""
Secure file serving utilities.

Demonstrates the path traversal vulnerability and its mitigation.
"""

import os
from typing import Optional


def is_safe_filename(filename: str) -> bool:
    """
    Check if a filename is safe (contains no path traversal sequences).

    Args:
        filename: The filename to validate.

    Returns:
        True if the filename is safe, False otherwise.
    """
    if not filename:
        return False

    if filename in ('.', '..'):
        return False

    if os.path.sep in filename or '/' in filename or '\\' in filename:
        return False

    if filename.startswith('.'):
        return False

    return True


def validate_file_path(base_dir: str, filename: str) -> Optional[str]:
    """
    Validate that a file path doesn't escape the base directory.

    SECURE: This function prevents path traversal attacks by:
    1. Validating the filename for unsafe characters
    2. Resolving both paths to absolute paths
    3. Checking that the resolved path stays within base_dir

    Args:
        base_dir: The allowed base directory.
        filename: The requested filename.

    Returns:
        Absolute path if valid and file exists, None otherwise.
    """
    if not is_safe_filename(filename):
        return None

    base_dir_abs = os.path.abspath(base_dir)
    requested_path = os.path.abspath(os.path.join(base_dir_abs, filename))

    # Critical check: ensure resolved path is within base_dir
    if not requested_path.startswith(base_dir_abs + os.sep):
        return None

    # Check if file exists
    if not os.path.isfile(requested_path):
        return None

    return requested_path


def read_file_safe(base_dir: str, filename: str) -> str:
    """
    Safely read a file from a base directory with path traversal protection.

    Args:
        base_dir: The allowed base directory.
        filename: The requested filename.

    Returns:
        The file contents as a string.

    Raises:
        PermissionError: If the path is invalid or traversal is attempted.
        FileNotFoundError: If the file does not exist.
    """
    filepath = validate_file_path(base_dir, filename)
    if filepath is None:
        raise PermissionError(f"Access denied: {filename}")

    with open(filepath, 'r') as f:
        return f.read()


# ============================================================================
# VULNERABLE VERSION - For educational comparison only.
# DO NOT USE IN PRODUCTION.
# ============================================================================


def read_file_vulnerable(base_dir: str, filename: str) -> str:
    """
    VULNERABLE: No path traversal protection.

    This function demonstrates the vulnerability. It directly joins
    the filename to the base directory without validation, allowing
    attackers to request files like '../../../etc/passwd'.

    Args:
        base_dir: The base directory.
        filename: The requested filename (can contain path traversal sequences).

    Returns:
        The file contents as a string.

    SECURITY NOTE: This function is intentionally vulnerable for educational
    purposes. Never use this pattern in production code.
    """
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r') as f:
        return f.read()
