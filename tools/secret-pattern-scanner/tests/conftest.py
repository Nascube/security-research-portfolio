"""Test fixtures and configuration."""

import os
import tempfile
import shutil
import pytest


@pytest.fixture
def temp_scan_dir():
    """Create temporary directory with test files."""
    tmpdir = tempfile.mkdtemp()

    # Create a config file with secrets
    with open(os.path.join(tmpdir, 'config.yml'), 'w') as f:
        f.write("""
database:
  host: localhost
  password: "db_password_SecurePass123"

aws:
  access_key: AKIAIOSFODNN7EXAMPLE
  secret: aws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

api:
  token: api_key = "sk-1234567890abcdefghijklmn"
""")

    # Create a .env file
    with open(os.path.join(tmpdir, '.env'), 'w') as f:
        f.write("""
DATABASE_PASSWORD=MySecretPassword123
API_KEY=sk-9876543210zyxwvutsrqponm
""")

    # Create a clean file (no secrets)
    with open(os.path.join(tmpdir, 'clean.txt'), 'w') as f:
        f.write("This is a normal file with no secrets.\n")

    yield tmpdir
    shutil.rmtree(tmpdir)
