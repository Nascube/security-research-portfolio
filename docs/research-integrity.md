# Research Integrity

This repository is a personal educational portfolio. Its usefulness — to the
author, to future readers, and to anyone evaluating the work — depends on
being honest about what has actually been done. This document is the
non-negotiable policy that keeps it that way.

---

## Core commitments

### 1. No fabricated findings

- No fake CVEs, no invented bug bounty payouts, no imagined incidents.
- No claim of vulnerability discovery unless a specific project directory
  contains verifiable evidence — a lab, a write-up, an issue link, or a
  disclosure record.
- No claim of professional penetration testing engagements unless supported
  by real work with real authorization from a real client.
- No invented employers, clients, coauthors, publications, or conference
  talks.

### 2. No borrowed credit

- Work produced by other people is cited, not re-labeled.
- Re-implementations of known techniques are labelled as such, in plain
  language, in the relevant project's README.
- Ideas encountered in blog posts, papers, or conversations are credited in
  a "Prior art & references" section — even when no code is reused.

### 3. Honest scope

- A learning exercise is presented as a learning exercise.
- A toy re-implementation is not sold as a production tool.
- Benchmarks and measurements state their setup and their limits — no
  cherry-picked "up to Nx faster" numbers without the underlying data in the
  repo.
- Negative results are welcome. A project that did not work, written up
  honestly, is a valid entry.

### 4. Corrections are versioned, not silently rewritten

- If a claim in this repository turns out to be wrong, the correction lands
  as a new commit that describes what changed and why.
- The wrong claim is not silently deleted from history.
- Where appropriate, a short `CORRECTIONS.md` note is added to the affected
  project.

### 5. Verification is a first-class artifact

- Every project has at least one automated or precisely documented
  verification step. See the [reproducibility policy](reproducibility.md).
- A running summary of what has actually been verified in this repository
  lives in [`verification-summary.md`](verification-summary.md).

## What "evidence in the repository" means

A claim is supported by evidence in the repository when at least one of the
following is true:

- **Code + tests.** The claim is embodied in code and exercised by a test a
  reader can run.
- **Reproducible measurement.** The claim is a measurement, and the
  repository contains the script that produced it plus the raw output.
- **Worked example.** The claim is a "this technique behaves like X", and
  the repository contains an example that demonstrates the behavior with
  committed inputs and outputs.
- **Verifiable citation.** The claim is a factual reference to public prior
  art, cited with a URL that a reader can follow (and, ideally, an archived
  link).

A claim supported only by the author's assertion is not, for the purposes of
this repository, supported.

## Handling of AI-assisted content

AI coding assistants are used in this repository as drafting tools. See the
[AI-assisted development methodology](../README.md#ai-assisted-development-methodology)
section of the main README. In the context of research integrity, three
rules apply:

1. **The author is responsible for every committed line.** "The assistant
   generated it" is not an excuse for a wrong claim.
2. **Assistants may not invent citations.** Every URL and every reference
   is checked by the author before commit.
3. **Assistants may not fabricate results.** Numbers, benchmarks, and
   outputs in the repository come from real runs on the author's machine,
   not from generated text.

## Handling of third-party content

- Third-party code is included only when its license allows it and it is
  credited in the project's README with the source URL and license.
- Third-party datasets are included only under a license that permits
  redistribution, or are fetched at reproduction time from a stable source
  with a recorded checksum.
- Screenshots, diagrams, and figures from third parties are used only under
  a license or a fair-use rationale that is stated inline.

## Responsible-use boundary

Research integrity here is inseparable from
[responsible use](../README.md#responsible-use). In particular:

- No claim in this repository will be supported by "evidence" that was
  gathered by unauthorized scanning, exploitation, or interaction with
  systems the author does not own.
- If a technique cannot be demonstrated inside a self-contained local lab,
  the write-up describes the technique in the abstract and cites public
  references, rather than manufacturing a live-target demonstration.

## Accountability

- The `git log` of this repository is the primary record. Author dates,
  commit messages, and diffs are the ground truth for what was done and
  when.
- Anyone who spots a factual error, a missing citation, an overclaim, or an
  integrity violation is invited to open an issue or PR (see
  [`CONTRIBUTING.md`](../CONTRIBUTING.md)).
- Substantiated integrity issues result in a correction commit and, where
  useful, an entry in the affected project's `CORRECTIONS.md`.
