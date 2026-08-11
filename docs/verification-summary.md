# Verification Summary

This document is the **running, honest inventory** of what has actually been
verified in this repository. It is deliberately minimal at the start of the
project's life and grows only when real work lands.

It exists so that a reader — including a future version of the author — can
tell, at a glance, the difference between:

- **Claims backed by verifiable work in this repository**, and
- **Aspirations, scaffolding, or in-progress items.**

If a project or claim is not listed here, it should not be treated as
verified, no matter how it is framed elsewhere.

---

## Status legend

| Status         | Meaning                                                                 |
| -------------- | ----------------------------------------------------------------------- |
| ✅ Verified    | Reproducible in this repository; independently checkable by a reader.    |
| 🧪 In progress | Work has started; verification is not yet complete.                     |
| 📝 Planned     | Documented intent only; no code or evidence has landed.                 |
| ⚠️ Retracted   | Was claimed previously; has been withdrawn. See linked correction note. |

## Repository-level items

| Item                                        | Status     | Evidence                                                 |
| ------------------------------------------- | ---------- | -------------------------------------------------------- |
| Repository scaffolding and policy documents | ✅ Verified | This commit — `README.md`, `SECURITY.md`, `CONTRIBUTING.md`, `LICENSE`, `.gitignore`, `docs/*.md`, section READMEs. |
| Directory structure matches the README      | ✅ Verified | `research/`, `labs/`, `tools/` exist with per-directory READMEs. |
| License is present and consistent           | ✅ Verified | [`LICENSE`](../LICENSE) (MIT) referenced from `README.md`. |
| Security reporting process is documented    | ✅ Verified | [`SECURITY.md`](../SECURITY.md).                          |
| Reproducibility policy is documented        | ✅ Verified | [`docs/reproducibility.md`](reproducibility.md).          |
| Research integrity policy is documented     | ✅ Verified | [`docs/research-integrity.md`](research-integrity.md).    |

## Project-level items

| Path | Status | Evidence |
|------|--------|----------|
| labs/secure-file-serving/ | ✅ Verified | 61 pytest tests pass (30 Flask HTTP endpoints + 31 secure implementation + 7 vulnerable demonstration). 86% coverage of core logic. Demonstrates path traversal vulnerability (CWE-22) and its fix. Secure implementation blocks traversal attacks; vulnerable version shows the problem. Dockerfile and docker-compose.yml valid. See [secure-file-serving/README.md](../labs/secure-file-serving/README.md). |
| tools/secret-pattern-scanner/ | ✅ Verified | 18 pytest tests pass (10 detector pattern tests + 8 file scanner tests). Demonstrates pattern-based secret detection with synthetic test data. Used to audit this repository. See [secret-pattern-scanner/README.md](../tools/secret-pattern-scanner/README.md). |

## What is explicitly **not** claimed at this time

To keep the record honest, the following are called out as **not** claimed by
this repository:

- No CVEs discovered by the author.
- No bug bounty payouts.
- No professional penetration testing engagements.
- No published papers, conference talks, or industry disclosures.
- No production security tooling deployed at scale.

These are listed here not because they are impossible outcomes, but because
this document exists precisely to prevent quiet drift between what the
repository actually contains and how it is described elsewhere. If any of
these change, they will be added as verified rows with links to the
supporting evidence — never as prose in a README without a corresponding
entry here.

## How this document is maintained

- Every PR that adds or removes a project also updates this document.
- Entries move from 📝 Planned → 🧪 In progress → ✅ Verified only when the
  linked evidence exists in the repository.
- Retractions are added as ⚠️ Retracted rows with a link to the correction
  commit or note. Previous rows are not silently deleted.
