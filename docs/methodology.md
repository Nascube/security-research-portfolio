# Methodology

This document describes how work in this repository is planned, executed, and
written up. It is deliberately opinionated: consistent methodology is what
makes the results in the [research/](../research/), [labs/](../labs/), and
[tools/](../tools/) directories comparable to each other and reproducible by a
reader.

## Guiding principles

1. **A project is a written record, not a demo.** If it cannot be described
   clearly in a README, it is not finished.
2. **Small, self-contained, reproducible.** Prefer many small projects that
   run end-to-end over one large project that only mostly works.
3. **Evidence in the repo, or the claim does not exist.** Any assertion about
   behavior, performance, or security must be backed by code, data, or a
   verifiable citation in the same directory.
4. **Failure is a finding.** An experiment that did not work, written up
   honestly, is a valid entry.

## Lifecycle of a project

Each project — whether a lab, a research note, or a tool — follows the same
lifecycle:

### 1. Framing

Before any code is written, the project's README stub answers:

- **Question.** What is being investigated or built, in one sentence?
- **Scope.** What is explicitly *in* and *out* of scope? Is this a local,
  self-contained exercise?
- **Success criterion.** How will the author know the project is done?
- **Prior art.** What has already been written or built in this area? At
  minimum, a short list of URLs.

If the framing cannot be written, the project is not ready to start.

### 2. Design

A short design section is added to the project README:

- **Approach.** The technique or architecture chosen, and why.
- **Alternatives considered.** At least one alternative and why it was
  rejected.
- **Assumptions.** OS, language version, hardware, and any other environment
  assumptions.
- **Ethics / scope guardrails.** For anything security-adjacent, a short note
  on how the project stays inside the
  [responsible-use boundaries](../README.md#responsible-use).

### 3. Implementation

- Code lives in the project directory. No shared "utils" pile at the top of
  the repository unless it is genuinely reused by multiple projects.
- Dependencies are pinned. `requirements.txt`, `package-lock.json`,
  `Cargo.lock`, or the equivalent is committed.
- Formatting and linting run cleanly before commit.

### 4. Verification

Every project has at least one form of verification:

- A test (unit, property-based, or integration) that a reader can run.
- A reproducible measurement with a documented expected result.
- A worked example whose output is either committed or precisely described.

The [reproducibility policy](reproducibility.md) defines the minimum bar.

### 5. Write-up

The final README section is a plain-language write-up:

- **What was built.**
- **What was learned.** Including negative results.
- **Limitations.** Honest scope of what the result actually shows.
- **Next steps**, if any, phrased as open questions rather than promises.

### 6. Post-mortem (optional but encouraged)

For non-trivial projects, a short retrospective note captures what surprised
the author. These are useful signal for future work and, over time, they
become a personal knowledge base.

## Documentation standards

- **Markdown, Github-flavored.** All prose is Markdown. Diagrams live as
  either inline Mermaid or committed SVG.
- **Every project README has a "Scope" section near the top.** This is where
  the project states what it will and will not claim.
- **Every project README has a "Reproduce" section.** This is where the
  reader learns the exact commands to re-run the project.
- **Every project README has an "Attribution" section** if any third-party
  content is used, per the
  [attribution policy](../README.md#attribution-policy).
- **Citations use full URLs** and, where possible, an archived link.

## Threat-model-first for defensive projects

For anything defensive (a validator, a hardening exercise, a detection
write-up), the project README opens with a short threat model:

- **Assets.** What is being protected?
- **Adversaries.** What kind of attacker is in scope?
- **Assumptions.** What is trusted?
- **Non-goals.** What this defense explicitly does not address.

This keeps defensive claims honest and prevents scope creep from "this
mitigates X" to "this mitigates everything."

## Version discipline

- Every project's README lists the language, runtime, and OS versions it was
  developed and tested against.
- If a project stops working on a newer version of a dependency, the
  breakage is documented before it is fixed, so the record shows what
  actually changed.

## AI-assisted work

See the
[AI-assisted development methodology](../README.md#ai-assisted-development-methodology)
section of the main README. The short version: assistants may help draft,
refactor, and document, but the author is responsible for every committed
line, and no assistant is permitted to fabricate results or citations.
