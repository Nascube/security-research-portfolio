# research/

Written analyses, notes, and study projects. This directory is for work
whose primary deliverable is a **document** — a walk-through, a comparison,
a threat model, a literature note — rather than a runnable artifact.

Runnable, self-contained experiments belong in [`../labs/`](../labs/).
Reusable original utilities belong in [`../tools/`](../tools/).

---

## Scope

- **In scope:** literature notes and syntheses; threat models; defensive
  design walk-throughs; comparisons of documented techniques; annotated
  reading lists; post-mortems of the author's own experiments.
- **Out of scope:** anything that would violate
  [responsible use](../README.md#responsible-use) — no live-target
  reconnaissance, no unauthorized testing, no offensive playbooks against
  third parties.
- **Out of scope:** narrative claims of "discoveries" without evidence.
  Discovery-type claims belong in a lab with a reproducible demonstration.

## Layout

Each project is a subdirectory named in kebab-case, e.g.:

```
research/
├── README.md                       ← this file
└── some-topic-note/                ← example (does not exist yet)
    ├── README.md
    ├── references.md
    └── figures/
```

Every project directory contains at least a `README.md`. Where a project
cites external sources, a `references.md` (or an equivalent section in the
README) lists them with full URLs and, where possible, archived links.

## What a "finished" research entry looks like

At minimum, the project README covers:

1. **Question.** What is being investigated, in one sentence.
2. **Scope.** In/out of scope, and any responsible-use guardrails.
3. **Background.** A short summary of relevant prior art, with citations.
4. **Analysis.** The actual write-up.
5. **Limitations.** What the analysis does *not* show.
6. **References.** Full citations for every claim that depends on external
   material.
7. **Attribution.** Any third-party figures, quotes, or data used, with
   licenses.

Entries follow the general [methodology](../docs/methodology.md) and, when
they cite measurements, the
[reproducibility policy](../docs/reproducibility.md).

## Verification

Verified research entries appear in
[`../docs/verification-summary.md`](../docs/verification-summary.md). At the
time of the initial commit, no research entries have landed.
