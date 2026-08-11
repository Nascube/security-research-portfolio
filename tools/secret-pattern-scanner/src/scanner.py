"""
Secret pattern scanner - detects accidentally committed secrets in files.
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Tuple


class SecretDetector:
    """Detect secret patterns in text."""

    # Secret patterns (regex)
    PATTERNS = {
        'AWS_KEY': r'AKIA[0-9A-Z]{16}',
        'AWS_SECRET': r'aws_secret_access_key\s*[:=]\s*["\']?[A-Za-z0-9/+=]{40}["\']?',
        'PRIVATE_KEY': r'-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) (?:PRIVATE |ENCRYPTED )?KEY',
        'API_TOKEN': r'(?:api|secret|token)[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9\-_.]{20,}["\']?',
        'BEARER_TOKEN': r'bearer\s+[a-zA-Z0-9\-_.]{20,}',
        'PASSWORD': r'password["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',
    }

    def __init__(self):
        self.compiled_patterns = {
            name: re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for name, pattern in self.PATTERNS.items()
        }

    def detect(self, content: str) -> List[Dict]:
        """
        Detect secrets in content.

        Args:
            content: File content to scan

        Returns:
            List of detected secrets with line numbers and pattern names
        """
        findings = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for pattern_name, regex in self.compiled_patterns.items():
                matches = regex.finditer(line)
                for match in matches:
                    findings.append({
                        'line': line_num,
                        'pattern': pattern_name,
                        'match': match.group(0),
                    })

        return findings

    def is_likely_secret(self, match_text: str) -> bool:
        """
        Filter out false positives.
        A likely secret has sufficient entropy and proper length.
        """
        # Exclude example/test patterns
        if any(x in match_text.lower() for x in ['example', 'test', 'demo', 'fake', 'YOUR_']):
            return False

        # Must be long enough
        if len(match_text) < 10:
            return False

        return True


class FileScanner:
    """Scan files for secrets."""

    EXTENSIONS = {'.py', '.yaml', '.yml', '.json', '.env', '.txt', '.md', '.js', '.ts'}

    def __init__(self):
        self.detector = SecretDetector()
        self.results = {}

    def scan_file(self, filepath: str) -> Dict:
        """
        Scan a single file.

        Args:
            filepath: Path to file

        Returns:
            Dict with scan results
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e), 'findings': []}

        findings = self.detector.detect(content)

        # Filter out false positives
        filtered_findings = [
            f for f in findings
            if self.detector.is_likely_secret(f['match'])
        ]

        return {
            'file': filepath,
            'findings': filtered_findings,
            'total': len(filtered_findings),
        }

    def scan_directory(self, directory: str) -> Dict:
        """
        Scan all files in a directory.

        Args:
            directory: Directory path

        Returns:
            Dict with aggregated results
        """
        results = {
            'directory': directory,
            'files_scanned': 0,
            'secrets_found': 0,
            'files': []
        }

        path = Path(directory)
        if not path.exists():
            return results

        # Scan all files recursively
        for file_path in path.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.EXTENSIONS:
                result = self.scan_file(str(file_path))
                if 'error' not in result:
                    results['files_scanned'] += 1
                    if result['total'] > 0:
                        results['secrets_found'] += result['total']
                        results['files'].append(result)

        return results

    def report(self, results: Dict) -> str:
        """Format scan results as a report."""
        lines = []
        lines.append(f"Scanned {results['files_scanned']} files")
        lines.append(f"Found {results['secrets_found']} potential secrets\n")

        for file_result in results['files']:
            lines.append(f"File: {file_result['file']}")
            for finding in file_result['findings']:
                lines.append(
                    f"  Line {finding['line']}: {finding['pattern']} - {finding['match'][:30]}..."
                )
            lines.append("")

        return '\n'.join(lines)
