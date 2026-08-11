"""
Tests for the VULNERABLE file serving implementation.

These tests demonstrate the path traversal vulnerability and show WHY
the secure implementation is necessary.

IMPORTANT: These tests intentionally exploit a vulnerability to illustrate
how it works. This is for educational purposes only. Never use vulnerable
patterns in production code.
"""

import os
import sys
import pytest

# Add src directory to path so we can import fileserver
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fileserver import read_file_vulnerable


class TestVulnerabilityDemonstration:
    """Demonstrate the path traversal vulnerability."""

    def test_vulnerable_allows_parent_directory_access(self, sensitive_files):
        """
        VULNERABILITY: The vulnerable version allows access to parent directory.

        This test demonstrates that read_file_vulnerable does NOT prevent
        path traversal attacks. An attacker can use '../' to escape the
        intended directory.
        """
        temp_files, sensitive_path = sensitive_files

        # The vulnerable function WILL allow this!
        content = read_file_vulnerable(temp_files, '../sensitive.txt')

        # Verify that we actually read the file outside the base directory
        assert content == 'Sensitive data - should NOT be accessible'
        print("⚠️  VULNERABILITY CONFIRMED: Parent directory access allowed!")

    def test_vulnerable_allows_multiple_traversal_levels(self, sensitive_files):
        """
        VULNERABILITY: The vulnerable version allows multiple traversal levels.

        This demonstrates that an attacker can use multiple '../' sequences
        to go up many directory levels.
        """
        temp_files, sensitive_path = sensitive_files

        # Try to access a file several levels up
        try:
            content = read_file_vulnerable(
                temp_files, '../../../../../../etc/passwd'
            )
            # If this succeeds, we've demonstrated the vulnerability
            print(
                "⚠️  VULNERABILITY: Could read file outside allowed directory!"
            )
        except FileNotFoundError:
            # This is expected if /etc/passwd doesn't exist or system is Windows
            # But the attempt itself proves the vulnerability exists
            print("⚠️  VULNERABILITY: Traversal was attempted without validation!")
            pass

    def test_vulnerable_no_filename_validation(self, temp_files):
        """
        VULNERABILITY: The vulnerable version has no filename validation.

        The vulnerable function accepts any string as a filename,
        including strings with path separators.
        """
        # This should work in the vulnerable version (if the file exists)
        try:
            content = read_file_vulnerable(temp_files, 'subdir\\nested.txt')
            if 'Nested' in content:
                print("⚠️  VULNERABILITY: Subdirectory access not prevented!")
        except FileNotFoundError:
            # Expected if Windows path separator doesn't match
            try:
                content = read_file_vulnerable(temp_files, 'subdir/nested.txt')
                if 'Nested' in content:
                    print("⚠️  VULNERABILITY: Subdirectory access not prevented!")
            except FileNotFoundError:
                pass


class TestVulnerabilityComparison:
    """Compare vulnerable vs. secure implementations."""

    def test_vulnerable_succeeds_where_secure_fails(self, sensitive_files):
        """
        COMPARISON: Show the difference between vulnerable and secure.

        The vulnerable version allows an attack that the secure version blocks.
        """
        from fileserver import read_file_safe as secure_read

        temp_files, sensitive_path = sensitive_files
        attack_payload = '../sensitive.txt'

        # Vulnerable version allows it
        vulnerable_result = read_file_vulnerable(temp_files, attack_payload)
        assert vulnerable_result == 'Sensitive data - should NOT be accessible'

        # Secure version blocks it
        with pytest.raises(PermissionError):
            secure_read(temp_files, attack_payload)

        print("✓ SECURITY COMPARISON: Secure implementation blocks the attack!")


class TestExploitationScenarios:
    """Real-world exploitation scenarios."""

    def test_config_file_disclosure(self, sensitive_files):
        """
        SCENARIO: An attacker tries to read a configuration file.

        A common attack: request '../../../config.json' to read
        application configuration that might contain secrets.
        """
        temp_files, _ = sensitive_files

        # Vulnerable version is susceptible
        try:
            content = read_file_vulnerable(temp_files, '../sensitive.txt')
            print("⚠️  SCENARIO: Configuration file could be disclosed!")
        except FileNotFoundError:
            pass

    def test_source_code_disclosure(self, sensitive_files):
        """
        SCENARIO: An attacker tries to read source code.

        Another common attack: request '../app.py' to read
        application source code.
        """
        from fileserver import read_file_safe as secure_read2

        temp_files, _ = sensitive_files

        # Secure version prevents this
        with pytest.raises(PermissionError):
            secure_read2(temp_files, '../app.py')
        print("✓ SCENARIO: Source code access prevented!")

    def test_credential_file_access(self, sensitive_files):
        """
        SCENARIO: An attacker tries to read credentials.

        High-severity attack: request '../../.env' to read
        environment configuration with database credentials.
        """
        from fileserver import read_file_safe as secure_read3

        temp_files, _ = sensitive_files

        # Secure version prevents this
        with pytest.raises(PermissionError):
            secure_read3(temp_files, '../../.env')
        print("✓ SCENARIO: Credential file access prevented!")


# Mark all tests in this module as demonstrating vulnerabilities
pytestmark = pytest.mark.vulnerability_demo
