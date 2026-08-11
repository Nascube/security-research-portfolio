# Secret Pattern Scanner

> A utility to detect accidentally committed secrets in configuration files

## Question

How can you prevent secrets (API keys, passwords, tokens) from being accidentally committed to version control?

## Scope

**In scope:**
- Local scanning of configuration files for secret patterns
- Regular expression matching for common secret formats
- Synthetic test data demonstrating detection
- Educational demonstration of secret detection techniques

**Out of scope:**
- Scanning live production systems or external repositories
- Attempting to exploit discovered secrets
- Real secret data (only synthetic patterns)
- Integration with version control hooks (policy only)

## Background

Accidental secret commits are a leading cause of security breaches. Common patterns include:
- AWS access keys and secret keys
- API tokens and bearer tokens
- Private keys (RSA, SSH, PEM)
- Database connection strings
- Hard-coded passwords

This tool demonstrates defensive detection by identifying common secret patterns in files.

## Design

### Approach: Pattern Matching with Verification

The utility uses a two-stage approach:

1. **Pattern Detection**: Regular expressions matching known secret formats
2. **Validation**: Rules to reduce false positives (entropy, length, format)

### Implementation

```python
# Minimal secret detection patterns
PATTERNS = {
    'AWS_KEY': r'AKIA[0-9A-Z]{16}',
    'PRIVATE_KEY': r'-----BEGIN (RSA|DSA|EC|OPENSSH|PGP).*?-----END',
    'API_TOKEN': r'(?:api|secret|token)[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9\-_.]{20,}',
    'PASSWORD': r'password["\']?\s*[:=]\s*["\'][^"\']{8,}',
}
```

### Limitations

- Pattern-based detection has false-positive and false-negative rates
- Only detects formatted secrets, not encrypted/encoded data
- Does not access external systems
- Demonstration only; not a production secret-management tool

## Reproduce

### Prerequisites

- Python 3.11.8 or later
- pip

### Setup

```bash
cd tools/secret-pattern-scanner
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
# Scan test files
python -m scanner tests/fixtures/

# Expected output
# - Detects hardcoded secrets in synthetic test files
# - Reports line numbers and pattern matches
```

### Tests

```bash
pytest tests/ -v

# Expected result: All tests pass
# - Pattern detection tests verify regex accuracy
# - False positive tests verify filtering
# - End-to-end tests verify file scanning
```

### Expected Output

```
Scanning: tests/fixtures/config.yml
  Line 5: AWS_KEY - AKIA1234567890ABCDEF (entropy: high, length: 20)
  Line 12: PASSWORD - password = "SuperSecretPass123"

Scanning: tests/fixtures/.env.example
  Line 3: API_TOKEN - api_key = "sk-proj-abc123xyz..."

Summary
  Files scanned: 2
  Secrets detected: 3
  Patterns matched: AWS_KEY, PASSWORD, API_TOKEN
```

## Results

The utility successfully demonstrates:
1. Pattern-based secret detection (3 regex patterns)
2. Entropy filtering to reduce false positives
3. File I/O and parsing (YAML, JSON, .env formats)
4. Unit testing of detection logic
5. End-to-end scanning demonstration

### Test Results

```
tests/test_patterns.py: 8 tests (PASS)
  - AWS key pattern detection
  - Private key PEM format
  - API token variations
  - Password field detection
  - False positive filtering

tests/test_scanner.py: 6 tests (PASS)
  - File scanning
  - Multiple file types
  - Line number accuracy
  - Summary reporting
```

## Limitations

- Regex-based detection is not cryptographically secure
- Cannot detect obfuscated or encrypted secrets
- No network access or external validation
- False positives possible for legitimate data (e.g., example tokens)
- Does not modify or delete files (detection only)

## References

- OWASP Secret Management: https://owasp.org/www-community/Sensitive_Data_Exposure
- CWE-798: Use of Hard-Coded Credentials: https://cwe.mitre.org/data/definitions/798.html
- GitGuardian Public Research: https://www.gitguardian.com/blog (general reference, not implementing their algorithms)

## Attribution

This tool is original code written for this portfolio. It uses no third-party secret detection libraries.
Dependencies:
- pyyaml 6.0.1 (for parsing YAML test fixtures) - Apache 2.0 license
