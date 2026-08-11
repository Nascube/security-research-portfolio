"""Pytest configuration and fixtures."""

import os
import tempfile
import shutil
import pytest


@pytest.fixture
def temp_files():
    """Create a temporary directory with test files."""
    tmpdir = tempfile.mkdtemp()

    # Create test files inside the temporary directory
    with open(os.path.join(tmpdir, 'hello.txt'), 'w') as f:
        f.write('Hello World')

    with open(os.path.join(tmpdir, 'secret.txt'), 'w') as f:
        f.write('Secret data - should be accessible')

    # Create a subdirectory (should not be accessible)
    os.makedirs(os.path.join(tmpdir, 'subdir'), exist_ok=True)
    with open(os.path.join(tmpdir, 'subdir', 'nested.txt'), 'w') as f:
        f.write('Nested file - should not be accessible')

    yield tmpdir

    # Cleanup
    shutil.rmtree(tmpdir)


@pytest.fixture
def sensitive_files(temp_files):
    """Create files outside the base directory to test traversal attempts."""
    parent_dir = os.path.dirname(temp_files)

    # Create a sensitive file in the parent directory
    sensitive_path = os.path.join(parent_dir, 'sensitive.txt')
    with open(sensitive_path, 'w') as f:
        f.write('Sensitive data - should NOT be accessible')

    yield temp_files, sensitive_path

    # Cleanup
    if os.path.exists(sensitive_path):
        os.remove(sensitive_path)
