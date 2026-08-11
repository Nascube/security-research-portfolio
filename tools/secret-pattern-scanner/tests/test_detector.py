"""Tests for SecretDetector class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from scanner import SecretDetector


class TestPatternMatching:
    """Test that patterns correctly detect secrets."""

    def test_aws_key_pattern(self):
        """AWS access keys should be detected."""
        detector = SecretDetector()
        content = "aws_key = AKIAIOSFODNN7EXAMPLE"
        findings = detector.detect(content)
        assert len(findings) > 0
        assert any(f['pattern'] == 'AWS_KEY' for f in findings)

    def test_password_pattern(self):
        """Password fields should be detected."""
        detector = SecretDetector()
        content = 'password = "SuperSecurePass123"'
        findings = detector.detect(content)
        assert len(findings) > 0
        assert any(f['pattern'] == 'PASSWORD' for f in findings)

    def test_api_token_pattern(self):
        """API tokens should be detected."""
        detector = SecretDetector()
        content = 'api_key = "sk-1234567890abcdefghij"'
        findings = detector.detect(content)
        assert len(findings) > 0
        assert any(f['pattern'] == 'API_TOKEN' for f in findings)

    def test_bearer_token_pattern(self):
        """Bearer tokens should be detected."""
        detector = SecretDetector()
        content = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        findings = detector.detect(content)
        assert len(findings) > 0

    def test_private_key_pattern(self):
        """Private key headers should be detected."""
        detector = SecretDetector()
        content = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890
-----END RSA PRIVATE KEY-----"""
        findings = detector.detect(content)
        assert len(findings) > 0

    def test_line_number_accuracy(self):
        """Line numbers should be correct."""
        detector = SecretDetector()
        content = """line 1
line 2
password = "Secret123"
line 4"""
        findings = detector.detect(content)
        if findings:
            assert findings[0]['line'] == 3

    def test_no_false_positives_for_example(self):
        """'example' in content should reduce false positives."""
        detector = SecretDetector()
        # Example text with token format
        is_likely = detector.is_likely_secret("api_token_example_value_12345")
        assert is_likely == False

    def test_no_false_positives_for_test(self):
        """'test' in content should reduce false positives."""
        detector = SecretDetector()
        is_likely = detector.is_likely_secret("test_password_abc123def456")
        assert is_likely == False

    def test_requires_minimum_length(self):
        """Short strings should not be considered secrets."""
        detector = SecretDetector()
        is_likely = detector.is_likely_secret("short")
        assert is_likely == False

    def test_clean_content_no_findings(self):
        """Files with no secrets should have no findings."""
        detector = SecretDetector()
        content = "This is a normal README file with no secrets."
        findings = detector.detect(content)
        # No findings that pass the is_likely_secret filter
        likely_findings = [
            f for f in findings
            if detector.is_likely_secret(f['match'])
        ]
        assert len(likely_findings) == 0
