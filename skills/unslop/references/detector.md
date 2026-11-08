# Detector workflow

Use the bundled detector to rank files for review. Set `UNSLOP_SKILL_DIR` to the
absolute directory containing `SKILL.md` and run from the writing target.
`--no-project` avoids loading that project's dependencies.

```shell
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" FILE_OR_DIR
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" -v docs/
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" --json report.json FILE_OR_DIR
```

Use `.` when no target is supplied. `-v` includes low-severity findings; `--json`
writes a machine-readable report. Follow [scope rules](../SKILL.md#choose-the-target)
before editing: scores do not authorize changes.

Read the text regardless of score. Regex cannot judge meaning or voice and misses
contextual problems covered by [the taxonomy](ai-writing-patterns.md).
