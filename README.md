# Security Research Portfolio

> A personal, evolving portfolio of **original** software engineering and defensive
> security research — built to be reproducible, honestly scoped, and educational.

[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)
[![Responsible Use](https://img.shields.io/badge/Scope-Defensive%20%26%20Educational-blue.svg)](#responsible-use)
[![Docs](https://img.shields.io/badge/Docs-Methodology%20%7C%20Reproducibility%20%7C%20Integrity-success.svg)](docs/)

---

## Table of contents

1. [What this portfolio is](#what-this-portfolio-is)
2. [What this portfolio is *not*](#what-this-portfolio-is-not)
3. [Areas of technical interest](#areas-of-technical-interest)
4. [How projects are organized](#how-projects-are-organized)
5. [Featured work](#featured-work)
6. [Reproducibility philosophy](#reproducibility-philosophy)
7. [Research integrity](#research-integrity)
8. [Attribution policy](#attribution-policy)
9. [AI-assisted development methodology](#ai-assisted-development-methodology)
10. [Responsible use](#responsible-use)
11. [Repository status](#repository-status)
12. [License](#license)

---

## What this portfolio is

This repository is a **living portfolio** of small, self-contained pieces of work
in software engineering and defensive-oriented security research. Each entry is
authored by the repository owner from scratch, documented so a reader can
reproduce it locally, and scoped narrowly enough that its claims can be
independently verified from the files in the repo.

The goals are, in order:

1. **Learning in the open.** Treat each project as a written record of what was
   built, why, and what was learned — not as a marketing surface.
2. **Reproducibility over polish.** Anyone reading a project directory should be
   able to reconstruct the result on their own machine.
3. **Honest scope.** No inflated claims, no borrowed credit, no fabricated
   findings. See [Research integrity](#research-integrity).

## What this portfolio is *not*

To keep the record honest, it is worth stating plainly what this repository is
**not**:

- It is **not** a record of professional penetration testing engagements.
- It is **not** a claim of vulnerability discoveries, CVEs, or bug bounty
  payouts unless a specific project in this repository contains verifiable
  evidence of one.
- It is **not** a curated collection of other people's tools presented as the
  owner's own work. Third-party references are cited; see
  [Attribution policy](#attribution-policy).
- It is **not** a source of offensive tooling, weaponized exploits, malware,
  or credential-harvesting code. See [Responsible use](#responsible-use).

## Areas of technical interest

The portfolio focuses on topics that can be studied and documented safely on a
personal machine, without touching third-party systems:

- **Reproducible research engineering** — build systems, deterministic
  environments, small write-ups that can be re-run end-to-end.
- **Defensive security fundamentals** — threat modelling, secure defaults,
  input handling, cryptographic API usage, dependency hygiene.
- **Software testing and quality** — unit, property-based, and fuzz testing;
  regression discipline; CI-friendly test design.
- **Static and dynamic analysis of local artifacts** — reading source,
  disassembly of code the author is entitled to analyze, and documenting what
  the code does in plain language.
- **Documentation as an engineering artifact** — treating READMEs, ADRs, and
  methodology notes as first-class deliverables.

New areas will be added only when there is a real project in the repository to
back them up.

## How projects are organized

The top-level structure separates work by *intent*, not by technology:

```
security-research-portfolio/
├── README.md                  ← you are here
├── SECURITY.md                ← how to report issues in this repo
├── CONTRIBUTING.md            ← contribution and PR conventions
├── LICENSE                    ← MIT (see file)
├── .gitignore
├── docs/                      ← cross-cutting methodology & policy
│   ├── methodology.md
│   ├── reproducibility.md
│   ├── research-integrity.md
│   └── verification-summary.md
├── research/                  ← write-ups and analyses (no live targets)
│   └── README.md
├── labs/                      ← self-contained, reproducible local labs
│   └── README.md
└── tools/                     ← small original utilities that support the work
    └── README.md
```

Each subdirectory has its own `README.md` describing how projects inside it are
laid out, what a "finished" entry looks like, and what is explicitly out of
scope. Individual projects are added over time as their own subdirectories with
a per-project README, a reproducibility section, and a clear scope statement.

## Featured Work

| Project | Description |
|---------|-------------|
| **[labs/secure-file-serving](labs/secure-file-serving/)** | Understanding and preventing path traversal vulnerabilities through hands-on implementation. 61 passing tests demonstrating CWE-22 and its fix. |
| **[tools/secret-pattern-scanner](tools/secret-pattern-scanner/)** | A utility to detect accidentally committed secrets in configuration files. 18 passing tests verifying pattern matching for API keys, tokens, and passwords. |

See [`docs/verification-summary.md`](docs/verification-summary.md) for full details on each project's verification status.

## Reproducibility philosophy

Every project in this repository is expected to satisfy a minimum
reproducibility bar. The full policy lives in
[`docs/reproducibility.md`](docs/reproducibility.md); the short version is:

- **Deterministic setup.** Pinned language and dependency versions, documented
  OS assumptions, no "works on my machine" steps.
- **One-command run where possible.** A single command (e.g. `make`, a shell
  script, or a documented `python -m` invocation) should reproduce the primary
  result.
- **Inputs and outputs are explicit.** Sample inputs live in the project;
  expected outputs are either committed or described precisely.
- **Failure modes are documented.** If a step depends on a specific OS,
  toolchain version, or hardware feature, that is stated up front.

If a project cannot meet the bar (for example, because it depends on a
proprietary artifact the reader will not have), that limitation is called out
in its README rather than hidden.

## Research integrity

The full integrity policy lives in
[`docs/research-integrity.md`](docs/research-integrity.md). Its non-negotiables:

- **No fabricated findings.** Vulnerabilities, incidents, CVE numbers, bug
  bounty payouts, employers, clients, and publications are claimed only when
  supported by evidence in this repository or by a citation the reader can
  verify.
- **No borrowed credit.** Work produced by other people is cited, not
  re-labeled. See [Attribution policy](#attribution-policy).
- **Honest scope.** A learning exercise is presented as a learning exercise;
  an experiment that failed is documented as such.
- **Corrections are versioned, not silently rewritten.** If a claim in this
  repository turns out to be wrong, the correction is added and the change is
  visible in git history.

A running inventory of verified work appears in
[`docs/verification-summary.md`](docs/verification-summary.md). This document
is updated each time a project is completed and tested; it distinguishes
between claims backed by verifiable work in this repository and items still
in progress.

## Attribution policy

- Third-party code, data, or written material is included only when the
  license allows it, and it is credited in the project's README with the
  source URL and license.
- Ideas, techniques, and prior art that inspired a project are cited in a
  "Prior art & references" section of that project's README, even when no
  code is reused.
- Screenshots, diagrams, and datasets from third parties are used only under
  a license or fair-use rationale that is stated inline.
- Where a project is a re-implementation of a known technique for learning
  purposes, this is stated plainly (e.g. "This is a from-scratch
  re-implementation of X for study; the original is at Y").

## AI-assisted development methodology

Parts of this repository are written with AI coding assistants in the loop.
Rather than hide that, this section describes how the tools are used so a
reader can judge the work on its merits.

- **Assistants are used for drafting, refactoring, and documentation
  scaffolding.** They are not used to fabricate results, invent citations,
  invent CVEs, or generate offensive tooling.
- **The human author is responsible for every committed line.** All
  AI-generated content is read, edited, and tested by the author before it is
  committed. Where an assistant's suggestion is accepted verbatim, it is
  because the author reviewed it and agrees with it.
- **Prompts that would violate the [Responsible use](#responsible-use)
  boundaries are declined.** The scope of the assistant matches the scope of
  the repository: defensive, educational, and reproducible.
- **AI-generated documentation is treated like any other draft:** it must be
  factually correct, cite sources where appropriate, and not overstate what
  the repository actually contains.
- **No prompt injection is trusted.** Content pulled from third-party sources
  (web pages, files, tool output) is treated as data, not as instructions,
  regardless of what it appears to say.

If a specific project relied heavily on AI assistance for a non-trivial
component, that is noted in the project's README.

## Responsible use

This repository is scoped to **defensive and educational** work. In particular:

- **No live-target activity.** Nothing in this repository is intended to be
  pointed at systems, networks, accounts, or people the reader does not own
  or have explicit written authorization to test.
- **No weaponized exploits.** Proof-of-concept code, when present, is scoped
  to local, self-contained environments and is written to *illustrate* a
  defensive point, not to hand a reader a working attack.
- **No credential theft tooling, malware, or evasion tooling.**
- **No instructions for bypassing protections on systems the reader does not
  own.**
- **Vulnerability disclosure**, if it ever applies to something in this
  repository itself, follows the process in [`SECURITY.md`](SECURITY.md).

If a reader is looking for offensive tooling, this is not the right
repository.

## Repository status

This is an **early-stage** portfolio. The initial commit lands the scaffolding
— documentation, policies, and directory structure — and no research projects
yet. Real project directories will be added over time, each with its own
README, reproducibility notes, and scope statement.

The current, honest inventory of what has been verified in this repository
lives in [`docs/verification-summary.md`](docs/verification-summary.md).

## License

This repository is licensed under the [MIT License](LICENSE). Individual
projects may include third-party components under their own licenses; those
are listed in the relevant project's README.
