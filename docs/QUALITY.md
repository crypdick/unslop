# Quality scorecard

Assessed on 2026-09-09. The table compares verification scope across repository
areas. Grades reflect measured checks, not detector accuracy.

| Area | Coverage | Types | Maximum complexity | Test health | Grade |
| --- | --- | --- | --- | --- | --- |
| CLI and file discovery | 100% line/branch | strict mypy | 9 | files, stdin, JSON, errors, terminal output | A |
| Scanner and reports | 100% line/branch | strict mypy | 13 | scoring, signal categories, clean prose, formatting | A |
| Pattern tables | 100% line/branch | strict mypy | no functions | category and representative phrase checks | A |
| Rewrite skill and taxonomy | not executable Python | not applicable | not applicable | manual corpus; constraints checked automatically | B |
| Development hooks | outside runtime coverage | strict mypy | Ruff limit 15 | linting and hook smoke checks | B |

The suite has 137 tests. Pytest uses at most four workers and a 20-second per-test
timeout. Coverage includes CLI subprocesses and every runtime module under
`scripts/`; development hooks and the trivial `__main__` dispatch are excluded.
No network recordings are needed because the tests make no external service calls.
Mypy checks tests but allows unannotated test definitions. Production and hook
functions must satisfy the full strict configuration.

`uv run prek run --all-files` runs hygiene, secrets, lock freshness, schema,
dependency, dead-code, type, formatting, complexity, custom checks, and tests.
CI runs the same command. `uv run pytest` prints uncovered lines as a fix list and
writes a browsable report to `htmlcov/index.html`. The coverage floor stays at 100%.

## Maintain the grades

Update this scorecard when verification scope changes materially or a domain loses
coverage or type safety. Grade A means the area's applicable automated gates pass
and its observable behavior is tested; B identifies a substantive manual or
unmeasured component; C identifies a failing gate or known behavior defect.
Measure complexity with Ruff rather than adding a second complexity tool.

## Documentation gardening

When changing scanner behavior, review README usage and exit codes, the skill's
taxonomy, and the evaluation corpus in the same change. Exercise changed CLI
examples and follow code `NOTE:` back-pointers. When changing the skill prompt,
manually rewrite the corpus inputs and verify every `must_preserve` and
`must_avoid` constraint; corpus schema tests alone do not evaluate model rewrites.

Twice a year, review `ARCHITECTURE.md` against module ownership and imports, run
README examples in a fresh environment, and fix stale instructions. This manual
review is the doc-gardening mechanism for this small plugin.
