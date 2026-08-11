# Security Policy

This document describes how to report security issues **in this repository
itself** — for example, a bug in a script under `tools/`, a mistake in a lab
under `labs/`, or a documentation defect that could mislead a reader in a
security-relevant way.

This policy does **not** apply to third-party systems, products, or services.
Nothing in this repository is intended to be used against systems the reader
does not own or have explicit written authorization to test. See the
[Responsible use](README.md#responsible-use) section of the main README.

---

## Scope

In scope for a report to this repository:

- Bugs in original code shipped under this repository (`tools/`, `labs/`,
  `research/`, or any future project directory).
- Documentation that could reasonably lead a reader to take an unsafe action
  (e.g., unclear scope statements, missing warnings on a lab, incorrect
  reproducibility instructions).
- Accidental inclusion of secrets, credentials, private keys, personal data,
  or copyrighted material owned by a third party.
- Supply-chain concerns about dependencies pinned by this repository.

Out of scope:

- Issues in third-party projects that this repository merely references or
  cites. Please report those to the upstream maintainers.
- Findings against live production systems belonging to other parties. This
  repository does not accept, host, or forward such reports.
- General feature requests or design opinions — please use a regular issue or
  pull request for those.

## How to report

Preferred channel:

- **GitHub Security Advisories.** Open a private advisory on the repository
  ("Security" tab → "Report a vulnerability"). This keeps the discussion
  private until a fix is ready.

Alternative channel:

- **Private issue via email**, if a public email address for the repository
  owner is listed on their GitHub profile. Please include the word
  `security` in the subject line.

Please do **not** open a public GitHub issue for a suspected security problem
until it has been triaged.

## What to include

A useful report typically includes:

1. The affected file(s) and, where possible, a specific commit hash.
2. A short description of the issue and why it is a concern.
3. A minimal reproduction — commands, inputs, expected vs. actual output.
4. Your assessment of impact and any suggested remediation.
5. Whether you would like to be credited in the fix (see below).

## What happens next

This is a personal educational repository maintained on a best-effort basis.
The maintainer will:

1. Acknowledge receipt of a valid report, typically within a few days.
2. Investigate and confirm or dispute the finding.
3. Prepare a fix, add a test or documentation change that prevents
   regression where practical, and land it in a normal commit.
4. Credit the reporter in the commit message or a `CHANGELOG` entry if the
   reporter has asked to be credited.

There is **no bug bounty**, no financial reward, and no service-level
agreement. Reporters who follow this policy in good faith will be treated
with courtesy and credited by name (or anonymously, per their preference).

## Handling of secrets

If a report concerns accidentally committed secrets:

- The maintainer will revoke and rotate the affected credential first, then
  purge it from history (`git filter-repo` or equivalent) and force-push,
  documenting the incident in a `docs/` note.
- Please do **not** publish the leaked secret in a public issue while it is
  still valid.

## A note on offensive testing

This repository does not authorize offensive testing against any system.
Sending unsolicited findings that rely on unauthorized scanning, exploitation,
or interaction with third-party infrastructure is out of scope and will not
be acted on.
