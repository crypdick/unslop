# Detector workflow

Use the bundled detector to triage files, especially for directory or batch requests. Set `UNSLOP_SKILL_DIR` to the absolute directory containing `SKILL.md`. Keep the current working directory at the writing target so relative paths retain their meaning. `--no-project` prevents uv from loading that project's dependencies.

```shell
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" FILE_OR_DIR
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" -v docs/
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" --json report.json FILE_OR_DIR
```

For an invocation without a target, use `.` as `FILE_OR_DIR`, show ranked candidates, and confirm scope before editing unless already authorized. Once scoped, edit files in place using the main skill's workflow.

The detector scores vocabulary clusters, formulaic phrases, and dangling participles. Verbose mode includes low-severity findings; JSON supports batch or CI use.

Read the text even when the detector finds nothing. Regex cannot judge information value, supported significance, authorial voice, or whether synonym changes make prose harder to follow. It can also miss unfamiliar promotional wording, stacked hedges, and formulaic conclusions. Use [the taxonomy](ai-writing-patterns.md) and editorial judgment; scores alone do not authorize edits.
