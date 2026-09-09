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

The detection script and skill reference a taxonomy of AI writing patterns organized by severity:

- **Tier 1 (dead giveaways):** vocabulary clusters ("delve", "tapestry", "pivotal", "robust"), copulative avoidance ("serves as" instead of "is"), formulaic significance framing ("is a testament to"), the "not just X, but Y" construction
- **Tier 2 (strong signals):** promotional tone, dangling participle filler clauses, rule-of-three abuse, synonym cycling, vague attribution ("experts argue"), formulaic conclusions, and false ranges
- **Tier 3 (contextual tells):** decorative punctuation and compression, manufactured sentence rhythm, pseudo-agency, unexplained jargon, decorative analogies, ambiguous references, stacked rhetorical questions, transition spam, and templated structure

The script's scores help you choose which files to review. The skill also looks for problems that regular expressions cannot judge, such as unsupported claims of importance and explanations that add no information. Findings are editing cues, not proof that AI wrote the text.

## Development

Prepare the development environment and run checks with these commands:

```shell
uv sync --locked                       # install the locked development tools
uv run prek install                    # enable Git hooks
uv run prek run --all-files             # run all quality gates
uv run pytest                          # tests and 100% branch coverage
uv run scripts/detect_slop.py -v docs/   # scan documentation
```

The scanner also runs with plain Python 3.13 or later and has no runtime
dependencies. Coverage includes command-line subprocesses. View the report in
`htmlcov/index.html`. See [the design conventions](CONVENTIONS.md),
[the architecture map](docs/ARCHITECTURE.md), and
[the quality scorecard](docs/QUALITY.md) for development guidance.

If you have the `new-feature` command-line tool installed, `new-feature create NAME --no-agent`
creates an isolated worktree and runs the setup configured in `pyproject.toml`.
Replace `NAME` with your feature name. Change into the printed worktree path to
work there. Each worktree has its own environment and test caches. No services
or credentials need setup.

`evals/rewrite_cases.json` contains manual rewrite cases with facts that must survive and phrases the final edit should remove. Use it when changing the skill prompt or comparing model behavior.
