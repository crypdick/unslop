# unslop

A [Claude Code plugin](https://docs.claude.com/en/docs/claude-code-plugins) for editing AI-sounding text. It helps remove filler, exaggerated claims, and repetitive phrasing while preserving the author's meaning and voice.

## What it does

**As a skill:** Say "unslop this" or "make this sound human" to have the agent edit your text in context. It checks for problems such as stacked hedges, unnecessary structure, and forced synonym changes.

**As a script:** `detect_slop.py` uses regular expressions to score files for review. It detects patterns such as vocabulary clusters, formulaic phrases, and dangling participles. Use it to scan a directory or check files in CI.

## Install

Add the following configuration to your Claude Code `settings.json` file:

```json
{
  "enabledPlugins": {
    "unslop@unslop": true
  },
  "extraKnownMarketplaces": {
    "unslop": {
      "source": {
        "source": "github",
        "repo": "crypdick/unslop"
      }
    }
  }
}
```

Then restart Claude Code or run `/reload-plugins`.

For a standalone skill installation, copy `skills/unslop/`. It contains the detector
and its runtime modules as regular files, so GitHub ZIP installs also work. The skill
commands resolve the detector from the installed skill directory.

## Usage

### Skill (interactive)

In any Claude Code conversation, enter either of these prompts:

```text
unslop this paragraph
```

```text
/unslop
```

Paste text that sounds like AI wrote it and ask Claude to clean it up. The skill triggers on phrases such as "unslop", "de-slop", "remove AI writing", and "sounds like ChatGPT".

### Script (batch scanning)

Scan files with the following commands. Replace `FILE_OR_DIR` with a file or directory path:

```shell
uv run scripts/detect_slop.py FILE_OR_DIR       # scan files
uv run scripts/detect_slop.py -v docs/           # verbose (show low-severity)
uv run scripts/detect_slop.py --json report.json  # JSON output
uv run scripts/detect_slop.py --threshold 3.0 src/  # only flag high-scoring files
echo "some text" | uv run scripts/detect_slop.py -   # stdin
```

Exit code `0` means no score exceeds the threshold, `1` means a score exceeds it,
and `2` means invalid arguments or no matching text files.

## What it catches

The [taxonomy](skills/unslop/references/ai-writing-patterns.md) groups patterns by review priority:

- **Tier 1:** stock vocabulary clusters, empty significance claims, and formulaic contrasts.
- **Tier 2:** promotional tone, vague attribution, repetition, and over-explanation.
- **Tier 3:** contextual cues such as decorative punctuation, jargon, and templated structure.

Scores help prioritize review. The skill also judges meaning and voice, which
regex cannot assess. Findings are editing cues, not proof of AI authorship.

## Development

Set up and check changes:

```shell
uv sync --locked                       # install the locked development tools
uv run prek install                    # enable Git hooks
uv run prek run --all-files             # run all quality gates
uv run pytest                          # tests and 100% branch coverage
uv run scripts/detect_slop.py -v docs/   # scan documentation
```

The scanner also runs with plain Python 3.13 or later and has no runtime
dependencies. Coverage includes command-line subprocesses. View the report in
`htmlcov/index.html`. See [design conventions](CONVENTIONS.md) and
[verification guidance](docs/QUALITY.md) for development guidance.

For an isolated worktree, use `new-feature create NAME --no-agent` if installed.
It runs the setup in `pyproject.toml`; work from the printed path.

See [verification guidance](docs/QUALITY.md) for manual rewrite evaluation.

### Plugin releases

After quality checks pass for a push to `main`, CI increments the patch version
and pushes a `Release X.Y.Z` commit. `pyproject.toml` is the version source of truth;
CI synchronizes `plugin.json`, `.claude-plugin/marketplace.json`, and
`.codex-plugin/plugin.json`, then refreshes `uv.lock` and checks the release before
pushing it. All manifests receive the same plain `major.minor.patch` version.

For a manual release, run `uv version --bump minor` (or `major` or `patch`) and
commit the result. CI preserves a version higher than the version before the push,
including a bump in an earlier commit of a multi-commit push. Decreased versions
fail release preparation. Feature branches and pull requests only run checks.
Retries reuse the release commit, and runs overtaken by another push skip release.

The release job uses the repository's `GITHUB_TOKEN` with `contents: write`.
Branch rules must allow that bot to push release commits. Bot pushes do not
trigger another workflow run; see [GitHub's token documentation](https://docs.github.com/en/actions/concepts/security/github_token).
