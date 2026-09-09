# Architecture

Unslop helps editors identify formulaic AI writing and rewrite it without losing
facts or voice. The plugin's skill supplies editorial judgment. An offline Python
scanner ranks files using regular expression matches and weighted findings. The
scanner does not call a model or perform rewrites.

## Codemap

The repository separates editing guidance, scanning, and development checks:

- `skills/unslop/SKILL.md` describes the editing workflow.
  `skills/unslop/references/ai-writing-patterns.md` contains its taxonomy.
- `scripts/detect_slop.py` is the command-line entry point. It discovers files,
  reads input, writes JSON, and chooses exit status. It also exports `scan_text`,
  `tokenize_lower`, `Finding`, and `FileReport` for callers.
- `scripts/slop_scanner.py` defines `Finding`, `FileReport`, and `Severity`.
  `scan_text` combines line and document signals into a weighted score.
- `scripts/slop_patterns.py` holds vocabulary and compiled regular expression tables.
- `scripts/slop_reports.py` formats findings and summaries for terminal output.
- `tests/` checks scanner and CLI behavior; `evals/rewrite_cases.json` supplies
  manual rewrite constraints and expected detector categories.
- `scripts/prek_hooks/` contains development checks invoked by `prek.toml`.
  Plugin manifests live in `plugin.json`, `.claude-plugin/`, and `.codex-plugin/`.

## Invariants

`detect_slop` imports `slop_scanner` and `slop_reports`; `slop_reports` imports
`slop_scanner`; `slop_scanner` imports `slop_patterns`. These arrows mean imports.
Patterns have no first-party imports. The scanner performs no filesystem,
terminal, or network I/O. Keep this small dependency graph reviewable without
adding a separate architectural linter.

Runtime modules use only the standard library and remain importable from
`scripts/`. No Python distribution or application service is deployed. Tests
configure that import path through pytest rather than modifying `sys.path`.
Development caches and environments stay inside each worktree, except uv's shared
package cache. No ports, databases, or credentials need allocation or copying.

Revisit this map twice a year, and when module ownership or import direction changes.
