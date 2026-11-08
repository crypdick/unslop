# Verification

`uv run prek run --all-files` runs the repository's quality gates locally and in
CI. `prek.toml` and `pyproject.toml` define the checks and thresholds.

Automated checks cover scanner and CLI behavior, standalone skill packaging,
release preparation, corpus constraints, linting, types, and repository hygiene.
Runtime and release code require 100% line and branch coverage, including CLI
subprocesses. Development hooks and trivial `__main__` dispatch are excluded.
Mypy is strict; test definitions may omit annotations.

Maintain canonical runtime code in root `scripts/` and synchronize its four
modules into `skills/unslop/scripts/` as regular files for standalone and GitHub
ZIP installs. Packaging tests reject links and differences between bundled
modules and their canonical sources.

Use focused tests during development. `uv run pytest` runs the suite, reports
uncovered lines, and writes `htmlcov/index.html`. Tests use no external services.

## Documentation and skill changes

Review documentation and evaluation cases affected by the change. Verify changed
CLI examples.

For editorial skill changes, use `evals/rewrite_cases.json` to check preservation
of meaning and removal of unwanted phrasing. Automated corpus checks validate
schema, grounded constraints, and declared detector categories; they do not
measure rewrite quality. Evaluate rewrites against `must_preserve` and
`must_avoid`, not detector scores alone.
