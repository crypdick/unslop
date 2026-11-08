# Design conventions

Keep the scanner small and offline. Preserve `python scripts/detect_slop.py`
usage. Development dependencies belong in uv's locked development group.

## Code and data

Prefer composed functions to detector class hierarchies. Use `Finding` and
`FileReport` for results, `Severity` for severity labels, and
`scripts/slop_patterns.py` for pattern tables. Use distinct types when they prevent
concrete caller mistakes, not for ordinary counts or indexes.

Keep file I/O, argument parsing, and JSON serialization in `detect_slop.py`;
scanner and formatter code work on text and typed reports. Parse structured
external data into typed records and validate value constraints at the boundary:
type annotations do not validate values.

Send diagnostics to stderr and reports to stdout. Catch specific expected I/O
errors and explain skipped files. If logging is needed, pass context through
`extra`.

## Behavior and maintenance

Test observable behavior through public entry points such as `scan_text`,
`collect_files`, and the CLI; do not import private first-party symbols.

Keep documentation, the skill taxonomy, detector patterns, and evaluation cases
consistent with changed behavior. Regex findings are editing cues, not proof of
AI authorship or rewrite quality.

Keep guidance focused on goals and essential constraints. Add procedural detail
when it prevents a concrete mistake or clarifies a non-obvious distinction; leave
routine choices to judgment. Preserve useful examples and rationale, not a target
word count.

Maintain the configured Ruff checks, strict mypy, 400-logical-line Python file
limit, and 100% production branch coverage. Keep check exceptions narrow and
explain why they are needed.
