# Contributing

Thanks for the interest. This is a personal educational portfolio, so the
contribution model is deliberately small and conservative. The goal is to keep
the repository honestly scoped, reproducible, and easy to verify.

Before opening a PR, please read the main [README](README.md), the
[research integrity policy](docs/research-integrity.md), and the
[reproducibility policy](docs/reproducibility.md). Those documents define
what the repository is willing to accept.

---

## What is welcome

- **Bug fixes** in existing code or documentation.
- **Reproducibility improvements** — better setup instructions, pinned
  versions, cleaner one-command runs.
- **Documentation improvements** — clearer scope statements, better
  attribution, corrections to factual errors, accessibility improvements.
- **Test additions** for existing code that lacks coverage.
- **Prior-art references** the current author was unaware of, added to the
  relevant project's "Prior art & references" section.

## What is not welcome

- **New offensive tooling**, weaponized proofs-of-concept, malware, or
  credential-harvesting code. See
  [Responsible use](README.md#responsible-use).
- **Findings against live third-party systems** — this repository does not
  accept, host, or forward such reports.
- **Verbatim copies of other people's projects** presented as original work.
- **Fabricated or unverifiable claims** — CVEs, employers, clients,
  publications, bounty payouts, or "discoveries" that are not backed by
  evidence in the repository or a citation the reader can verify.
- **Large speculative refactors** with no attached bug or user-visible
  improvement.

## Ground rules

1. **Every claim must be backed by evidence in the repository.** If your
   change adds a claim ("this technique detects X", "this measurement shows
   Y"), the evidence — code, data, or a citation — must land in the same PR.
2. **AI-assisted contributions are allowed**, on the same terms as the rest
   of the repository — see
   [AI-assisted development methodology](README.md#ai-assisted-development-methodology).
   You are responsible for every line you submit.
3. **Third-party content requires a compatible license and explicit
   attribution** in the relevant README. If in doubt, ask before opening the
   PR.
4. **No secrets in commits.** Not in code, not in tests, not in fixtures. If
   a test needs a credential-shaped value, use an obvious dummy
   (`"REDACTED-EXAMPLE-KEY"`).
5. **No PII or private data** in commits, ever, including in issue bodies.

## Pull request checklist

Before opening a PR, please confirm the following (a checklist in the PR body
is fine):

- [ ] The change is in scope per the README and the integrity policy.
- [ ] New code has at least a smoke test where practical.
- [ ] New or changed documentation renders correctly and links resolve.
- [ ] Third-party content is credited with source and license.
- [ ] No secrets, credentials, or personal data are included.
- [ ] Commit messages are clear and describe *why*, not just *what*.

## Commit style

- Prefer small, focused commits with imperative-mood subjects
  (`docs: clarify reproducibility bar` rather than `updated docs`).
- Reference the affected directory or project when useful
  (`labs/foo: fix build on Python 3.12`).
- If a commit fixes a specific issue, reference it in the body.

## Reporting security issues

Please **do not** open a public issue for a suspected security problem in this
repository. Follow the process in [`SECURITY.md`](SECURITY.md) instead.

## Code of conduct

See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Short version: be respectful,
be precise, and assume good faith. Personal attacks, harassment, and bad-faith
argumentation are not welcome and will result in the PR or issue being closed.
