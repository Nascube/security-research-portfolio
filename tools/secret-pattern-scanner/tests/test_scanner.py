"""Tests for FileScanner class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from scanner import FileScanner


class TestFileScanning:
    """Test that files are scanned correctly."""

    def test_scan_single_file(self, temp_scan_dir):
        """Scanning a file with secrets should find them."""
        scanner = FileScanner()
        result = scanner.scan_file(os.path.join(temp_scan_dir, 'config.yml'))
        assert result['total'] > 0
        assert len(result['findings']) > 0

    def test_scan_clean_file(self, temp_scan_dir):
        """Scanning a clean file should find nothing."""
        scanner = FileScanner()
        result = scanner.scan_file(os.path.join(temp_scan_dir, 'clean.txt'))
        assert result['total'] == 0
        assert len(result['findings']) == 0

    def test_scan_directory(self, temp_scan_dir):
        """Scanning a directory should scan all files."""
        scanner = FileScanner()
        results = scanner.scan_directory(temp_scan_dir)
        assert results['files_scanned'] >= 2  # At least config.yml and .env
        assert results['secrets_found'] > 0

    def test_report_generation(self, temp_scan_dir):
        """Report should be formatted correctly."""
        scanner = FileScanner()
        results = scanner.scan_directory(temp_scan_dir)
        report = scanner.report(results)
        assert "Scanned" in report
        assert "Found" in report
        assert len(report) > 0

    def test_env_file_detection(self, temp_scan_dir):
        """Should detect secrets in .env files."""
        scanner = FileScanner()
        result = scanner.scan_file(os.path.join(temp_scan_dir, '.env'))
        assert result['total'] > 0

    def test_multiple_secrets_per_file(self, temp_scan_dir):
        """Files with multiple secrets should report all of them."""
        scanner = FileScanner()
        result = scanner.scan_file(os.path.join(temp_scan_dir, 'config.yml'))
        # config.yml has multiple secret patterns
        assert result['total'] >= 2

    def test_nonexistent_directory_handling(self):
        """Scanning nonexistent directory should not crash."""
        scanner = FileScanner()
        results = scanner.scan_directory('/nonexistent/path/to/scan')
        assert results['files_scanned'] == 0
        assert results['secrets_found'] == 0

    def test_file_encoding_handling(self, temp_scan_dir):
        """Should handle various file encodings."""
        scanner = FileScanner()
        # Create file with UTF-8 content
        test_file = os.path.join(temp_scan_dir, 'utf8.txt')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('password = "test123"')

        result = scanner.scan_file(test_file)
        # Should not crash and should detect the pattern
        assert 'error' not in result or result['error'] is None
