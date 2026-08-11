# labs/

Self-contained, reproducible **local** experiments. Every lab is designed to
run on a single developer machine, with no live-target interaction and no
dependency on third-party infrastructure the reader does not control.

Written analyses without a runnable component belong in
[`../research/`](../research/). Reusable original utilities belong in
[`../tools/`](../tools/).

---

## Current Projects

### [secure-file-serving](secure-file-serving/)

**Path Traversal Vulnerability Prevention**

A hands-on lab demonstrating directory traversal (CWE-22) and its fix.
Includes a vulnerable implementation, a secure version with input validation
and path normalization, and 31 automated tests showing both the weakness and
the defense.

- **Language:** Python 3.11.8
- **Tests:** 31 pytest tests (all passing)
- **Docker:** Yes, with docker-compose.yml
- **Duration:** ~30 minutes to run and understand
- **Status:** ✅ Verified

See [`secure-file-serving/README.md`](secure-file-serving/README.md) for full details.

---

## Scope

- **In scope:** local, self-contained experiments — for example, small
  services running on `localhost`, containerized test environments,
  synthetic datasets, and defensive exercises against code the author owns.
- **Out of scope:** anything that touches systems, networks, accounts, or
  people that the reader does not own or have explicit written
  authorization to test. See
  [responsible use](../README.md#responsible-use).
- **Out of scope:** weaponized exploits, malware, credential-harvesting
  tooling, and detection-evasion tooling.

If a lab is security-adjacent, its README opens with a short threat model
per the [methodology](../docs/methodology.md#threat-model-first-for-defensive-projects).

## Layout

Each lab is a subdirectory named in kebab-case, e.g.:

```
labs/
├── README.md                       ← this file
└── some-lab/                       ← example (does not exist yet)
    ├── README.md
    ├── requirements.txt            ← or package.json / Cargo.toml / etc.
    ├── scripts/
    │   └── reproduce.sh
    ├── src/
    ├── tests/
    ├── fixtures/                   ← inputs and expected outputs
    └── ENVIRONMENT.md              ← optional; see reproducibility policy
```

Every lab must satisfy the
[reproducibility policy](../docs/reproducibility.md), including pinned
versions, a one-command primary result where practical, and at least one
verification step.

## What a "finished" lab looks like

At minimum, the lab README covers:

1. **Question / goal.** What the lab demonstrates, in one sentence.
2. **Scope.** In/out of scope, and the responsible-use guardrails.
3. **Threat model** (for defensive labs). Assets, adversaries, assumptions,
   non-goals.
4. **Design.** The approach chosen and at least one alternative considered.
5. **Reproduce.** OS + language versions; setup commands; the one command
   that produces the primary result; where to find expected output; how to
   run the automated verification.
6. **Results.** What actually happened, including negative results.
7. **Limitations.** Honest scope of what the lab shows.
8. **Attribution.** Third-party content with sources and licenses.

## Verification

Verified labs appear in
[`../docs/verification-summary.md`](../docs/verification-summary.md). At the
time of the initial commit, no labs have landed.
