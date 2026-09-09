# Design conventions

The scanner is a small, offline heuristic tool. Keep its runtime dependencies in
the Python standard library and preserve `python scripts/detect_slop.py` usage.
Development dependencies belong in the uv development group, with `uv.lock` tracked.

## Small functions and explicit data

Compose scanning functions instead of introducing detector class hierarchies.
`Finding` and `FileReport` carry results; pattern tables belong in
`scripts/slop_patterns.py`. Name shared code after its purpose. The file-length
hook limits Python files to 400 logical lines, including continuation lines.

Use `Severity` for the finite set of severity labels. Introduce `NewType` when two
otherwise identical scalar types represent distinct concepts that callers could
confuse. Do not wrap ordinary word counts or loop indexes without a concrete benefit.

## Parse at the boundary

Read files, parse command-line arguments, and serialize JSON in `detect_slop.py`.
Pass text and typed reports into the scanner and formatter. If a feature accepts
structured external data, parse it into a typed record and enforce its value
constraints there. Type annotations, `NewType`, and frozen dataclasses do not
validate untrusted values by themselves.

Keep diagnostics on stderr and report output on stdout. Catch specific expected
I/O errors and explain skipped files. Ruff owns print and logging checks; print is
allowed in these CLI and hook scripts. If logging is introduced, pass contextual
fields through `extra` instead of building messages with f-strings.

## Behavior and documentation

Test `scan_text`, `collect_files`, and CLI output or exit status. Tests must not
import private first-party symbols. Before changing behavior, add a failing test
that demonstrates the intended result, then implement and rerun it.

Keep `README.md`, the skill taxonomy, and detector patterns consistent. Add a
`NOTE:` back-pointer at code sites whose behavior is also specified in prose.
Regex signals are triage heuristics; passing tests does not prove a rewrite is
accurate or that flagged text was written by AI.

Maintain Ruff's curated rule set, strict mypy, and 100% production branch coverage.
Use narrow, explained exceptions only where a check misrepresents the code.
