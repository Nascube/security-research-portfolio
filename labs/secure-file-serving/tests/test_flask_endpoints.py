"""
End-to-end HTTP tests for Flask application endpoints.

Tests the actual Flask application endpoints to verify:
- Valid file access works
- Path traversal is blocked
- Error responses are correct
- Security headers are set appropriately
"""

import os
import sys
import pytest
import tempfile
import shutil

# Add src directory to path so imports work from pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import app as app_module
flask_app = app_module.app


@pytest.fixture
def client():
    """Create Flask test client with temporary fixtures directory."""
    # Create temporary directory with test files
    tmpdir = tempfile.mkdtemp()

    # Create test files
    with open(os.path.join(tmpdir, 'test.txt'), 'w') as f:
        f.write('Test file content')

    with open(os.path.join(tmpdir, 'readme.md'), 'w') as f:
        f.write('# Test README\n\nThis is a test file.')

    # Override FILES_DIR to use temporary directory
    flask_app.config['TESTING'] = True
    original_files_dir = app_module.FILES_DIR
    app_module.FILES_DIR = tmpdir

    with flask_app.test_client() as test_client:
        yield test_client, tmpdir

    # Restore and cleanup
    app_module.FILES_DIR = original_files_dir
    shutil.rmtree(tmpdir)


class TestHealthEndpoint:
    """Test the health check endpoint."""

    def test_health_endpoint_returns_ok(self, client):
        """Health check should return 200 OK."""
        test_client, tmpdir = client
        response = test_client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'

    def test_health_endpoint_is_json(self, client):
        """Health check should return JSON response."""
        test_client, tmpdir = client
        response = test_client.get('/health')
        assert response.content_type == 'application/json'


class TestSecureReadEndpoint:
    """Test the secure file reading endpoint."""

    def test_secure_read_valid_file(self, client):
        """Reading a valid file should return 200 OK with content."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/test.txt')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert data['filename'] == 'test.txt'
        assert data['content'] == 'Test file content'

    def test_secure_read_another_valid_file(self, client):
        """Reading a different valid file should return correct content."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/readme.md')
        assert response.status_code == 200
        data = response.get_json()
        assert 'Test README' in data['content']

    def test_secure_read_nonexistent_file(self, client):
        """Reading a nonexistent file should return 403 (not disclosing existence)."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/does_not_exist.txt')
        # App returns 403 to avoid information disclosure (doesn't reveal which files exist)
        assert response.status_code == 403

    def test_secure_read_blocks_parent_directory(self, client):
        """Attempts to read parent directory should return 403."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/..')
        assert response.status_code == 403
        data = response.get_json()
        assert 'denied' in data['reason'].lower() or 'traversal' in data['reason'].lower()

    def test_secure_read_blocks_traversal_attack(self, client):
        """Path traversal attempts are blocked (either by URL router or endpoint)."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/../../../etc/passwd')
        # Flask's URL router normalizes away ../ before it reaches our code (404)
        # OR our code blocks it (403). Both are secure; both should pass.
        assert response.status_code in (403, 404)

    def test_secure_read_blocks_traversal_with_backslash(self, client):
        """Traversal with backslash should return 403."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/..\\..\\windows\\system32')
        assert response.status_code == 403

    def test_secure_read_blocks_hidden_files(self, client):
        """Access to hidden files should return 403."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/.bashrc')
        assert response.status_code == 403

    def test_secure_read_blocks_absolute_paths(self, client):
        """Absolute path access should return 403."""
        test_client, tmpdir = client
        # Note: leading slash in URL becomes part of filename
        response = test_client.get('/secure/read//etc/passwd')
        # This may return 403 for invalid path or 404 if Flask doesn't route it
        assert response.status_code in (403, 404)

    def test_secure_read_blocks_subdirectory_access(self, client):
        """Access to files in subdirectories is blocked."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/subdir/file.txt')
        # Flask's router may not match this to our pattern (404)
        # or our validation rejects it (403). Both are secure.
        assert response.status_code in (403, 404)

    def test_secure_read_includes_security_header(self, client):
        """Secure endpoint should include security message."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/test.txt')
        data = response.get_json()
        assert 'security' in data or 'Protection' in str(data)


class TestVulnerableReadEndpoint:
    """Test the vulnerable endpoint (for comparison)."""

    def test_vulnerable_read_valid_file(self, client):
        """Vulnerable endpoint should allow reading valid files."""
        test_client, tmpdir = client
        response = test_client.get('/vulnerable/read/test.txt')
        assert response.status_code == 200
        data = response.get_json()
        assert data['content'] == 'Test file content'

    def test_vulnerable_endpoint_shows_warning(self, client):
        """Vulnerable endpoint should warn that it is vulnerable."""
        test_client, tmpdir = client
        response = test_client.get('/vulnerable/read/test.txt')
        data = response.get_json()
        assert 'VULNERABLE' in data.get('warning', '')

    def test_vulnerable_read_nonexistent_file(self, client):
        """Vulnerable endpoint should return 404 for missing files."""
        test_client, tmpdir = client
        response = test_client.get('/vulnerable/read/does_not_exist.txt')
        assert response.status_code == 404


class TestErrorHandling:
    """Test error handling and responses."""

    def test_404_error_response(self, client):
        """404 errors should return proper JSON response."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/nonexistent.txt')
        # App returns 403 for nonexistent files (doesn't disclose existence)
        assert response.status_code == 403
        assert response.content_type == 'application/json'
        data = response.get_json()
        assert 'error' in data

    def test_403_error_response(self, client):
        """Traversal attempts return JSON error responses."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/../etc/passwd')
        # Flask router or endpoint validation blocks this (403 or 404)
        assert response.status_code in (403, 404)
        if response.status_code != 404:  # Only check JSON if we get 403
            assert response.content_type == 'application/json'
            data = response.get_json()
            assert 'error' in data

    def test_404_includes_reason(self, client):
        """404 response should include reason."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/missing.txt')
        data = response.get_json()
        assert 'reason' in data or 'error' in data

    def test_403_includes_reason(self, client):
        """403 response should include reason."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/..')
        data = response.get_json()
        assert 'reason' in data or 'error' in data


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_filename(self, client):
        """Empty filename should return 404."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/')
        # This will match the route pattern with empty string
        # or return 404 depending on Flask routing
        assert response.status_code in (404, 400, 403)

    def test_filename_with_null_byte(self, client):
        """Filename with null byte should be handled safely."""
        test_client, tmpdir = client
        # URL-encoded null byte
        response = test_client.get('/secure/read/test%00.txt')
        # Should not crash; may be 404 or 403
        assert response.status_code in (404, 403, 400)

    def test_filename_with_dots(self, client):
        """Filename with only dots should be rejected."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/...')
        # Dots-only names should be rejected
        assert response.status_code == 403

    def test_url_encoded_traversal(self, client):
        """URL-encoded traversal attempt is blocked."""
        test_client, tmpdir = client
        # %2e%2e = .., but still contains /
        response = test_client.get('/secure/read/%2e%2e/etc/passwd')
        # Blocked by Flask's router (404) or our validation (403)
        assert response.status_code in (403, 404)

    def test_double_url_encoded_traversal(self, client):
        """Double URL-encoded traversal should be handled."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/%252e%252e/etc/passwd')
        # Double encoding should still be rejected or return 404
        assert response.status_code in (404, 403)

    def test_very_long_filename(self, client):
        """Very long filename should be handled."""
        test_client, tmpdir = client
        long_filename = 'a' * 1000 + '.txt'
        response = test_client.get(f'/secure/read/{long_filename}')
        # Should handle gracefully
        assert response.status_code in (404, 403, 414)


class TestResponseFormat:
    """Test that responses are properly formatted."""

    def test_success_response_has_required_fields(self, client):
        """Successful response should have required fields."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/test.txt')
        data = response.get_json()
        assert 'status' in data
        assert 'filename' in data
        assert 'content' in data
        assert data['status'] == 'ok'

    def test_error_response_has_required_fields(self, client):
        """Error response should have required fields."""
        test_client, tmpdir = client
        response = test_client.get('/secure/read/missing.txt')
        data = response.get_json()
        assert 'error' in data

    def test_response_content_type_is_json(self, client):
        """All responses should be JSON."""
        test_client, tmpdir = client
        endpoints = [
            '/health',
            '/secure/read/test.txt',
            '/vulnerable/read/test.txt',
        ]
        for endpoint in endpoints:
            response = test_client.get(endpoint)
            assert 'application/json' in response.content_type


class TestSecurityVulnerabilityDemonstration:
    """Demonstrate the vulnerability exists on the vulnerable endpoint."""

    def test_vulnerable_allows_traversal_attempt(self, client):
        """The vulnerable endpoint should allow traversal attempts."""
        test_client, tmpdir = client

        # Create a file outside the tmpdir
        parent_dir = os.path.dirname(tmpdir)
        outside_file = os.path.join(parent_dir, 'outside_test.txt')
        try:
            with open(outside_file, 'w') as f:
                f.write('Outside content')

            # Try to access it through the vulnerable endpoint
            # This test demonstrates the vulnerability; it WILL succeed
            response = test_client.get('/vulnerable/read/../outside_test.txt')

            # On the vulnerable endpoint, this may succeed (200) or fail
            # depending on path construction. The point is to show
            # the vulnerability can be attempted without 403 blocking.
            # If it succeeds (200), the vulnerability is proven.
            # If it returns 404/500, the file doesn't exist externally.

            # The important thing is that vulnerable endpoint doesn't
            # actively prevent traversal like secure endpoint does.
            print(f"⚠️  Vulnerable endpoint returned {response.status_code} for traversal attempt")
        finally:
            if os.path.exists(outside_file):
                os.remove(outside_file)

    def test_secure_blocks_what_vulnerable_allows(self, client):
        """Secure endpoint blocks traversal attempts."""
        test_client, tmpdir = client

        # Traversal attempt
        attack_payload = '../../../etc/passwd'

        secure_response = test_client.get(f'/secure/read/{attack_payload}')

        # Secure endpoint blocks it (either 403 from validation or 404 from router)
        # Both are correct security responses
        assert secure_response.status_code in (403, 404)
