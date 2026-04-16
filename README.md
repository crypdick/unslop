# unslop

A [Claude Code plugin](https://docs.claude.com/en/docs/claude-code-plugins) that detects and rewrites AI-sounding text. It catches the constellation of habits that make AI writing recognizable — inflated significance, empty hedging, compulsive structure, synonym cycling — and rewrites them into plain, direct prose.

## What it does

**As a skill:** Say "unslop this" (or "de-slop", "make this sound human", "sounds too AI", etc.) and it will rewrite your text as a human copyeditor would — cutting filler, deflating importance, and saying things straight. It preserves your ideas and register; it just removes the AI voice.

**As a script:** `detect_slop.py` is a regex-based scanner that triages files by slop density. It catches surface-level patterns (vocabulary clusters, formulaic phrases, dangling participles) and produces a per-file score. Useful for batch scanning and CI.

## Install

Add to your Claude Code `settings.json`:

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

## Usage

### Skill (interactive)

In any Claude Code conversation:

```
unslop this paragraph
```

```
/unslop
```

Paste text that sounds like AI wrote it and ask Claude to clean it up. The skill triggers on phrases like "unslop", "de-slop", "remove AI writing", "sounds like ChatGPT", etc.

### Script (batch scanning)

```bash
uv run scripts/detect_slop.py FILE_OR_DIR       # scan files
uv run scripts/detect_slop.py -v docs/           # verbose (show low-severity)
uv run scripts/detect_slop.py --json report.json  # JSON output
uv run scripts/detect_slop.py --threshold 3.0 src/  # only flag high-scoring files
echo "some text" | uv run scripts/detect_slop.py -   # stdin
```

Exit code 0 means clean, 1 means slop detected.

## What it catches

The detection script and skill reference a taxonomy of AI writing patterns organized by severity:

- **Tier 1 (dead giveaways):** vocabulary clusters ("delve", "tapestry", "pivotal", "robust"), copulative avoidance ("serves as" instead of "is"), formulaic significance framing ("is a testament to"), the "not just X, but Y" construction
- **Tier 2 (strong signals):** promotional tone, dangling participle filler clauses, rule-of-three abuse, synonym cycling, vague attribution ("experts argue"), formulaic conclusions ("despite challenges, the future looks promising")
- **Tier 3 (stylistic tells):** em dash overuse, hedge stacking, transition word spam, sycophantic openers, excessive boldface

The script catches what regex can. The skill catches what requires judgment — superficial analysis masquerading as depth, significance inflation with novel phrasing, and the general flatness of AI prose.

## Development

```bash
uv run pytest                          # run tests
uv run scripts/detect_slop.py -v .     # scan the repo itself
```
