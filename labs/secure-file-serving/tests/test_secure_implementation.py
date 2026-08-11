"""
Tests for the SECURE file serving implementation.

These tests demonstrate that the secure implementation correctly prevents
path traversal attacks while allowing legitimate file access.
"""

import os
import sys
import pytest

# Add src directory to path so we can import fileserver
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fileserver import (
    is_safe_filename,
    validate_file_path,
    read_file_safe,
)


class TestFilenameSafety:
    """Test filename validation logic."""

    def test_safe_filenames_are_accepted(self):
        """Normal filenames should pass validation."""
        assert is_safe_filename('hello.txt') is True
        assert is_safe_filename('README.md') is True
        assert is_safe_filename('file-123_test.pdf') is True
        assert is_safe_filename('report_2024.docx') is True

    def test_dot_dot_is_rejected(self):
        """Parent directory references (..) must be rejected."""
        assert is_safe_filename('..') is False
        assert is_safe_filename('../hello.txt') is False
        assert is_safe_filename('hello/../world.txt') is False

    def test_hidden_files_are_rejected(self):
        """Files starting with dot (hidden files) must be rejected."""
        assert is_safe_filename('.bashrc') is False
        assert is_safe_filename('.ssh') is False
        assert is_safe_filename('.hidden') is False

    def test_path_separators_are_rejected(self):
        """Path separators (/, \\) must be rejected."""
        assert is_safe_filename('path/to/file.txt') is False
        assert is_safe_filename('path\\to\\file.txt') is False
        assert is_safe_filename('subdir/file.txt') is False

    def test_traversal_attempts_are_rejected(self):
        """Various path traversal patterns must be rejected."""
        # Single level traversal
        assert is_safe_filename('../etc/passwd') is False
        # Multiple level traversal
        assert is_safe_filename('../../../../etc/passwd') is False
        # URL encoded (still contains slashes)
        assert is_safe_filename('..%2Fetc%2Fpasswd') is False
        # Backslash variant
        assert is_safe_filename('..\\..\\windows\\system32') is False

    def test_empty_and_none_are_rejected(self):
        """Empty and None values must be rejected."""
        assert is_safe_filename('') is False
        assert is_safe_filename(None) is False


class TestPathValidation:
    """Test path validation logic."""

    def test_valid_file_is_accessible(self, temp_files):
        """Valid files in the base directory should be accessible."""
        result = validate_file_path(temp_files, 'hello.txt')
        assert result is not None
        assert os.path.isfile(result)
        assert 'hello.txt' in result

    def test_invalid_filename_returns_none(self, temp_files):
        """Invalid filenames should return None."""
        result = validate_file_path(temp_files, '../etc/passwd')
        assert result is None

    def test_nonexistent_file_returns_none(self, temp_files):
        """Nonexistent files should return None."""
        result = validate_file_path(temp_files, 'does_not_exist.txt')
        assert result is None

    def test_traversal_to_parent_is_blocked(self, temp_files):
        """Attempts to traverse to parent directory are blocked."""
        result = validate_file_path(temp_files, '..')
        assert result is None

    def test_traversal_to_system_files_is_blocked(self, temp_files):
        """Attempts to access system files are blocked."""
        # Try to access /etc/passwd
        result = validate_file_path(temp_files, '../../../etc/passwd')
        assert result is None

    def test_subdirectory_traversal_is_blocked(self, temp_files):
        """Attempts to access files in subdirectories are blocked."""
        result = validate_file_path(temp_files, 'subdir/nested.txt')
        assert result is None

    def test_resolved_path_is_returned_for_valid_files(self, temp_files):
        """Valid files should return their absolute resolved path."""
        result = validate_file_path(temp_files, 'hello.txt')
        assert result is not None
        # Verify the path is absolute
        assert os.path.isabs(result)
        # Verify it's within the base directory
        assert result.startswith(os.path.abspath(temp_files))


class TestFileReading:
    """Test secure file reading."""

    def test_read_valid_file(self, temp_files):
        """Reading a valid file should succeed."""
        content = read_file_safe(temp_files, 'hello.txt')
        assert content == 'Hello World'

    def test_read_different_file(self, temp_files):
        """Reading different files should return correct content."""
        content = read_file_safe(temp_files, 'secret.txt')
        assert content == 'Secret data - should be accessible'

    def test_traversal_attempt_raises_permission_error(self, temp_files):
        """Traversal attempts should raise PermissionError."""
        with pytest.raises(PermissionError):
            read_file_safe(temp_files, '../etc/passwd')

    def test_parent_directory_raises_permission_error(self, temp_files):
        """Parent directory access should raise PermissionError."""
        with pytest.raises(PermissionError):
            read_file_safe(temp_files, '..')

    def test_hidden_file_raises_permission_error(self, temp_files):
        """Hidden file access should raise PermissionError."""
        with pytest.raises(PermissionError):
            read_file_safe(temp_files, '.bashrc')

    def test_nonexistent_file_raises_permission_error(self, temp_files):
        """Nonexistent files should raise PermissionError (not disclosing file existence)."""
        # Note: For security, we don't distinguish between "file doesn't exist"
        # and "path is invalid" - both return PermissionError to avoid
        # information disclosure attacks (e.g., timing attacks, directory enumeration).
        with pytest.raises(PermissionError):
            read_file_safe(temp_files, 'does_not_exist.txt')

    def test_subdirectory_access_raises_permission_error(self, temp_files):
        """Subdirectory access should raise PermissionError."""
        with pytest.raises(PermissionError):
            read_file_safe(temp_files, 'subdir/nested.txt')


class TestTraversalPreventionComprehensive:
    """Comprehensive traversal prevention tests."""

    def test_multiple_traversal_levels(self, temp_files):
        """Multiple levels of traversal should all be blocked."""
        attempts = [
            '../file.txt',
            '../../file.txt',
            '../../../etc/passwd',
            '../../../../etc/passwd',
            '../../../../../etc/passwd',
        ]
        for attempt in attempts:
            with pytest.raises(PermissionError):
                read_file_safe(temp_files, attempt)

    def test_mixed_separators(self, temp_files):
        """Mixed path separators should be blocked."""
        attempts = [
            '..\\..\\file.txt',
            '../..\\file.txt',
            '..\\../file.txt',
        ]
        for attempt in attempts:
            with pytest.raises(PermissionError):
                read_file_safe(temp_files, attempt)

    def test_absolute_paths_are_rejected(self, temp_files):
        """Absolute paths should be rejected."""
        attempts = [
            '/etc/passwd',
            'C:\\Windows\\System32\\drivers\\etc\\hosts',
        ]
        for attempt in attempts:
            with pytest.raises(PermissionError):
                read_file_safe(temp_files, attempt)

    def test_url_encoding_does_not_bypass_protection(self, temp_files):
        """URL encoding should not bypass protection."""
        # These are still invalid filenames (contain slashes)
        attempts = [
            '..%2Fetc%2Fpasswd',
            '%2Fetc%2Fpasswd',
        ]
        for attempt in attempts:
            with pytest.raises(PermissionError):
                read_file_safe(temp_files, attempt)
