# Working on unslop

Use `CONVENTIONS.md` for design constraints and `docs/QUALITY.md` for
verification scope.

Set up with `uv sync --locked` and `uv run prek install`. Before handoff, run
`uv run prek run --all-files`; use `--files` to include untracked changes.
For behavior changes, follow `.claude/agents.red-green-tdd.md`.

Record durable coding preferences in reliable automated checks where practical;
otherwise use `CONVENTIONS.md`.
