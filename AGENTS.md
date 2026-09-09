# Working on unslop

Read `CONVENTIONS.md` for design principles and `docs/ARCHITECTURE.md` for the codemap.
Run `uv sync --locked` to prepare the environment and `uv run prek install` to enable hooks.
Before handing off changes, run `uv run prek run --all-files`. Include untracked files
with `--files` when validating changes that have not been added to Git.

For behavior changes, follow `.claude/agents.red-green-tdd.md`.
Keep scanner tests on public entry points and retain the standard-library-only CLI.
Read `docs/QUALITY.md` for verification scope and documentation review guidance.
When the user expresses a coding preference, encode it in Ruff, prek, or a focused
hook when a reliable mechanical check is possible; otherwise update `CONVENTIONS.md`.
