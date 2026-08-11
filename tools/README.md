# tools/

Small **original** utilities that support work in the rest of the
repository. Tools live here when they are reusable across more than one lab
or research note, or when they are useful on their own as a defensive or
developer-productivity utility.

Written analyses belong in [`../research/`](../research/). Self-contained
experiments belong in [`../labs/`](../labs/).

---

## Scope

- **In scope:** original defensive or developer-productivity utilities —
  for example, a static-analysis helper, a small validator, a repository
  hygiene checker, or a fixture generator.
- **Out of scope:** offensive tooling, weaponized proofs-of-concept,
  malware, credential-harvesting utilities, network scanners intended for
  third-party targets, and detection-evasion tooling. See
  [responsible use](../README.md#responsible-use).
- **Out of scope:** thin wrappers around other people's tools presented as
  original work. If a project is a wrapper, it says so in its README and
  credits the underlying tool.

## Layout

Each tool is a subdirectory named in kebab-case, e.g.:

```
tools/
├── README.md                       ← this file
└── some-tool/                      ← example (does not exist yet)
    ├── README.md
    ├── pyproject.toml              ← or package.json / Cargo.toml / etc.
    ├── src/
    ├── tests/
    └── examples/
```

Every tool must satisfy the
[reproducibility policy](../docs/reproducibility.md) and ship with tests
proportional to its complexity.

## What a "finished" tool looks like

At minimum, the tool README covers:

1. **What it does.** One sentence.
2. **Scope.** What it will and will not do, and the responsible-use
   guardrails.
3. **Install.** Pinned language version; setup commands.
4. **Usage.** At least one worked example with expected output.
5. **Tests.** How to run them.
6. **Design notes.** Non-obvious choices and their rationale.
7. **Prior art & references.** Similar tools that already exist and how
   this one differs, or that it is intentionally a simpler learning
   re-implementation.
8. **Attribution.** Third-party dependencies of note, with licenses.

## Verification

Verified tools appear in
[`../docs/verification-summary.md`](../docs/verification-summary.md). At
the time of the initial commit, no tools have landed.
