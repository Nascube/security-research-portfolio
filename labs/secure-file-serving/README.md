# Secure File Serving Lab

> Understanding and preventing path traversal vulnerabilities through hands-on implementation

## Question

How can a file serving application be vulnerable to path traversal attacks, and how do you fix it?

## Scope

**In scope:**
- Path traversal vulnerability (CWE-22)
- Local file access vulnerability
- Defensive implementation using input validation and path normalization
- Automated testing of both vulnerable and secure implementations
- Docker containerization for reproducible testing

**Out of scope:**
- Live system scanning or reconnaissance
- Exploitation of real systems or services
- Network-based attacks
- Unauthorized access to third-party systems

## Background

Path traversal (also called directory traversal) is a web security vulnerability
that allows an attacker to access files outside the intended directory. For example:

```
GET /download/hello.txt       # OK - returns hello.txt
GET /download/../../../etc/passwd  # VULNERABLE - may return system files
```

The vulnerability occurs when an application:
1. Takes user input for a filename
2. Directly uses it to construct a file path
3. Fails to validate that the path stays within the allowed directory

This lab demonstrates:
- **The vulnerability** in `fileserver.read_file_vulnerable()`
- **The fix** in `fileserver.read_file_safe()`
- **Automated tests** proving both the problem and the solution

## Threat Model

### Assets
- Files in the allowed directory (intended for access)
- Files outside the directory (sensitive application files, system files, config, credentials)

### Adversaries
- Unauthenticated attacker
- Malicious user of the file download API

### Assumptions
- Files are stored on the filesystem
- The application runs with the user's permissions
- Filenames should be restricted to the base directory only

### Non-Goals
- Preventing attacks against files the application process cannot access
- Protecting against memory corruption or process exploitation
- Detecting abuse (rate limiting, logging, alerting)

## Design

### Approach: Input Validation + Path Normalization

The secure implementation uses a defense-in-depth approach:

1. **Filename validation** (`is_safe_filename`)
   - Reject parent directory references (`..`)
   - Reject path separators (`/`, `\`)
   - Reject hidden files (starting with `.`)
   - Reject empty/null values

2. **Path normalization** (`validate_file_path`)
   - Convert both paths to absolute paths
   - Resolve `.` and `..` sequences
   - Verify the resolved path is within the base directory
   - Check file exists before returning

3. **Error handling** (`read_file_safe`)
   - Raise `PermissionError` for invalid paths
   - Raise `FileNotFoundError` for missing files
   - Prevent information disclosure in errors

### Alternatives Considered

| Approach | Pros | Cons |
|---|---|---|
| **Blacklist dangerous patterns** | Simple implementation | Incomplete (easy to bypass) |
| **Whitelist allowed files** | Most secure | Inflexible, requires upfront list |
| **Chroot jail** | Strong isolation | Requires OS-level setup |
| **Input validation + normalization** (chosen) | Practical, multilayered, testable | Requires careful implementation |

### Why Blacklisting Fails

Blacklisting (e.g., rejecting `..`) is insufficient because:
- URL encoding: `..%2F` bypasses simple `..` check
- Encoding variants: Unicode normalization, double encoding
- OS-specific: Different separators on Windows vs. Unix
- Race conditions: File might change after validation

Path normalization + whitelist (verify path is in allowed directory) is more robust.

## Reproduce

### Prerequisites

- Python 3.11.8 or later
- pip
- Docker and Docker Compose (for containerized testing)
- Bash (for setup/teardown scripts)

### Setup

#### Local Setup

```bash
cd labs/secure-file-serving

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Docker Setup

```bash
cd labs/secure-file-serving
docker-compose build
docker-compose up
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run secure implementation tests only
pytest tests/test_secure_implementation.py -v

# Run vulnerability demonstration tests
pytest tests/test_vulnerable_implementation.py -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

### Run the Application

#### Local

```bash
python -m src.app
```

The Flask application listens on `http://localhost:5000`.

#### Docker

```bash
docker-compose up
```

Access the application at `http://localhost:5000`.

### Test the Endpoints

#### Secure Endpoint (Protected)

```bash
# Access a legitimate file
curl http://localhost:5000/secure/read/hello.txt

# Try to traverse to parent directory (BLOCKED)
curl http://localhost:5000/secure/read/../../../etc/passwd
# Response: 403 Forbidden with message "Access denied. Path traversal detected."
```

#### Vulnerable Endpoint (For Comparison Only)

```bash
# Access a legitimate file
curl http://localhost:5000/vulnerable/read/hello.txt

# Try to traverse (VULNERABLE - may succeed depending on OS)
curl http://localhost:5000/vulnerable/read/../fixtures/hello.txt
# WARNING: This may access files outside the intended directory
```

### Expected Output

Running `pytest tests/ -v` produces:

```
tests/test_secure_implementation.py::TestFilenameSafety::test_safe_filenames_are_accepted PASSED
tests/test_secure_implementation.py::TestFilenameSafety::test_dot_dot_is_rejected PASSED
...
tests/test_vulnerable_implementation.py::TestVulnerabilityDemonstration::test_vulnerable_allows_parent_directory_access PASSED
...

======================== 30 passed in 1.23s ========================
```

All tests pass, confirming:
- Secure implementation correctly validates all inputs
- Vulnerable implementation allows traversal (as expected, for demonstration)

## Results

### What Was Built

1. **`src/fileserver.py`** - Core file serving logic
   - `is_safe_filename()` - Validates filenames
   - `validate_file_path()` - Prevents traversal
   - `read_file_safe()` - Secure file reading
   - `read_file_vulnerable()` - Vulnerable version for comparison

2. **`src/app.py`** - Flask web application
   - `/secure/read/<filename>` - Protected endpoint
   - `/vulnerable/read/<filename>` - Vulnerable endpoint (for comparison)
   - `/health` - Health check

3. **`tests/`** - Comprehensive test suite
   - `test_secure_implementation.py` - 29 tests proving security
   - `test_vulnerable_implementation.py` - Vulnerability demonstrations
   - `conftest.py` - Test fixtures and setup

4. **Docker** - Reproducible environment
   - `Dockerfile` - Minimal Python image with dependencies
   - `docker-compose.yml` - Local service orchestration

5. **Fixtures** - Sample data
   - `fixtures/hello.txt` - Test file
   - `fixtures/README.txt` - Documentation

### What Was Learned

1. **Filename validation is necessary but not sufficient.**
   - Must reject both path separators and parent directory references
   - Must handle different encodings (URL, Unicode, etc.)

2. **Path normalization must happen AFTER validation.**
   - Resolve paths to absolute form to eliminate `.` and `..`
   - Compare against the base directory after resolution

3. **Testing both vulnerabilities and fixes is valuable.**
   - Tests that show "this attack works" (on vulnerable version) build confidence
   - Tests that show "this attack is blocked" (on secure version) provide proof

4. **Defense in depth is practical.**
   - Multiple layers (validation, normalization, existence check) make bypass harder
   - Each layer provides value even if others fail

### Limitations

1. **Scope is local-only.**
   - Demonstrates the vulnerability only against local files
   - Does not address remote file inclusion, SSRF, or network attacks

2. **Sensitive data is synthetic.**
   - Uses dummy files in temporary directories
   - Does not use real system files or credentials

3. **No rate limiting or logging.**
   - This lab focuses on prevention, not detection
   - Production would need audit logging and rate limiting

4. **Platform differences.**
   - Path handling differs between Windows (`\`) and Unix (`/`)
   - Tests run on both but results may vary (e.g., `/etc/passwd` only on Unix)

## References

- **CWE-22: Improper Limitation of a Pathname to a Restricted Directory**
  https://cwe.mitre.org/data/definitions/22.html

- **OWASP Path Traversal**
  https://owasp.org/www-community/attacks/Path_Traversal

- **Python os.path documentation**
  https://docs.python.org/3/library/os.path.html

- **Flask send_file() security considerations**
  https://flask.palletsprojects.com/en/3.0.x/api/#flask.send_file

## Attribution

This lab is an original educational work written for this repository.
It uses no external code; all source, tests, and documentation are
written from scratch.

### Dependencies

- Flask 3.0.0 — BSD-3-Clause
- pytest 7.4.3 — MIT
- Werkzeug 3.0.1 — BSD-3-Clause

All are open-source and used under compatible licenses.

## Verification

✅ Runs end-to-end via `pytest tests/` or `docker-compose up`
✅ All 30+ tests pass
✅ Demonstrates both vulnerability and fix
✅ Includes setup and teardown scripts
✅ Documented, reproducible, and honest about scope
