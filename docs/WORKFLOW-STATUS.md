# Legacy workflow status

The GitHub Actions failures retained for this repository are workflow-validation
failures: each discovered workflow was a zero-byte file, and each failed run had
zero jobs. The empty files implement no Python tests, builds, Pages deployment,
security analysis, or release. The source files and Git history remain preserved.

This repair moves only the empty workflow placeholders out of GitHub's active
`.github/workflows` directory, preserving their exact bytes under the names below.
Their Git blob identity is `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`.
Existing failed runs remain historical evidence; this does not turn them green.

| Original discovered path | Preserved placeholder |
|---|---|
| `.github/workflows/gh-pages (2).yml` | `docs/legacy-workflow-placeholders/gh-pages (2).yml.disabled` |
| `.github/workflows/gh-pages.yml` | `docs/legacy-workflow-placeholders/gh-pages.yml.disabled` |
| `.github/workflows/python (2).yml` | `docs/legacy-workflow-placeholders/python (2).yml.disabled` |
| `.github/workflows/python.yml` | `docs/legacy-workflow-placeholders/python.yml.disabled` |

The maintained [Avatar Suite](https://github.com/RobertMLayne/avatar-suite)
contains the integrated implementation, documented feature coverage, and actual
Windows/Linux validation. See its
[source and feature coverage](https://github.com/RobertMLayne/avatar-suite/blob/main/docs/FEATURE-COVERAGE.md).
That coverage records incomplete imports and empty packaging/docs scaffolds in
these originals, and keeps EXE/signing/site deployment as unresolved work.
The old README's build/deploy claims must therefore not be treated as delivered
behavior. This narrow workflow repair does not retire this source repository,
alter its license or visibility, or establish a working legacy release pipeline.

Validation on October 1, 2026: original workflow bytes and tracked Python source
hashes were checked before and after the move; all Python source remained
unchanged. `git diff --check` passed. The official API reported no main branch
protection and no rulesets at inspection time. No executable test or deployment
job existed in the archived files; none is claimed to have been run here.

Future build or deployment work must first supply real packaging/docs assets,
reproducible dependencies and meaningful tests. Any added workflows should use
minimum job permissions, verified action pins and bounded execution, following
Robert's development preferences and the actual workload.
