# Environment Attestation

This document captures the environment in which this lab was developed and tested.

## Development Environment

- **OS:** Windows 11 Pro, build 26200, 64-bit
- **Python:** 3.11.8 (primary)
- **Node.js:** v22.20.0
- **Docker:** 29.2.1, build a5c7197
- **Docker Compose:** v5.1.0

## Dependencies (Pinned Versions)

- Flask 3.0.0
- pytest 7.4.3
- pytest-cov 4.1.0
- Werkzeug 3.0.1

## Test Execution

- Tests run via `pytest tests/`
- All tests pass successfully
- Coverage reported via `pytest --cov=src tests/`

## Docker Build

- Base image: `python:3.11.8-slim`
- Non-root user: `appuser` (UID 1000)
- Exposed port: 5000
- Health check enabled via `/health` endpoint

## Known Limitations

- This lab uses synthetic data only. No real credentials or external services.
- The vulnerable implementation is intentionally unsafe for educational purposes.
- Path validation is filesystem-dependent and may behave differently on Windows vs. Linux.
  (This lab includes cross-platform tests to verify both work correctly.)

## Date of Attestation

Created and tested on 2026-08-12.
