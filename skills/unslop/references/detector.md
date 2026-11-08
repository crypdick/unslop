# Detector workflow

Use the bundled detector for file triage. Set `UNSLOP_SKILL_DIR` to the absolute directory containing `SKILL.md`; run from the writing target so relative paths resolve there. Keep `--no-project` to avoid loading the target project's dependencies.

```shell
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" FILE_OR_DIR
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" -v docs/
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" --json report.json FILE_OR_DIR
```

Without a target, use `.` as `FILE_OR_DIR`. Follow [the skill's scope rules](../SKILL.md#choose-the-target) before editing.

The detector scores vocabulary clusters, formulaic phrases, and dangling participles. `-v` includes low-severity findings; `--json` writes a machine-readable report.

Read the text even after a clean scan. Regex misses contextual problems and cannot judge meaning or voice. Use [the taxonomy](ai-writing-patterns.md) and editorial judgment; scores do not authorize edits.
