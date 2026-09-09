---
name: unslop
description: Clean up AI-sounding writing to read like a human wrote it. Use this skill whenever the user says "unslop", "de-slop", "remove AI writing", "make this sound human", "clean up AI tone", "fix AI voice", "sounds too AI", "sounds like ChatGPT", "too sloppy", "AI slop", or asks to remove, fix, or clean up signs of AI-generated text. Also trigger when the user pastes text that reads like obvious AI output and asks you to improve, rewrite, or edit it.
---

Edit AI-sounding text so it reads naturally while preserving the author's meaning and voice.

Watch for over-cutting. Removing function words and conjunctions can turn prose into a series of clipped statements. Keep the connective language that helps the reader follow a thought.

## Invocation

If the user provided text, a file path, or a directory: unslop that target.

If the user invoked the skill with **no arguments and no pasted text**, treat the current working directory as the target. Default workflow:

1. Set `UNSLOP_SKILL_DIR` as described under [Automated detection](#automated-detection-initial-pass-only), then run `uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" .` from the current working directory to triage which files have the worst slop.
2. Show the user the ranked list of offenders and confirm scope before editing (for example, "Top 5 files have slop. Want me to unslop all of them, or just the top N?").
3. Once confirmed, unslop the chosen files in place using the Edit tool, following the [rewriting principles](#rewriting-principles).

Only fall back to asking "what text do you want to clean?" if the current working directory has no candidate files (no `.md`, `.txt`, `.rst`, or other prose) or the detector finds nothing.

## Philosophy

Look for habits that recur together: inflated significance, empty hedging, unnecessary structure, and forced positivity. Read for the point the author is making, then say it plainly. Replacing a few flagged words is rarely enough.

Remove explanations and qualifications that add no information. Keep the detail the reader needs.

## Process

1. **Read the full text first.** Understand the author's point before editing.
2. **Identify the worst offenders.** Read `references/ai-writing-patterns.md` for the full taxonomy. Focus on patterns from Tier 1 and Tier 2 first. Treat Tier 3 as review cues, not automatic edits.
3. **Rewrite, don't just swap words.** Replacing "delve" with "explore" still sounds like AI. Restructure the sentence so it says something concrete instead of gesturing vaguely.
4. **Preserve the author's ideas.** You're removing the AI voice, not the content. If the text makes a substantive point, keep it. If a sentence is pure filler with no information content, cut it.
5. **Draft the rewrite privately.** Do not show an intermediate version.
6. **Run a private second-pass audit.** Check the draft for remaining Tier 1 and Tier 2 patterns, flattened rhythm, changed technical claims, lost uncertainty, and any opinion or detail you invented. Inspect Tier 3 patterns only when they cluster, repeat, obscure the meaning, or clash with the surrounding voice. Read it aloud mentally; if it sounds assembled or mechanically terse, revise it.
7. **Output only the final cleaned text**, then a brief summary of what you changed and why.

## Rewriting principles

### Say it straight

Bad: "The platform serves as a comprehensive solution that leverages cutting-edge technology to enhance user productivity."
Good: "The platform helps people get more done."

The original says nothing that the rewrite doesn't. All those extra words — "comprehensive," "leverages," "cutting-edge," "enhance" — are decoration, not information.

### Name actors and mechanisms

Vague abstractions can hide the only useful part of a sentence. Replace "This improved the process" with a supported, concrete relationship such as "Removing two fields shortened the signup form." Name who acted, what changed, or how the result happened when the source provides that information.

Do not invent a mechanism to make a vague claim sound precise. If the source does not support the explanation, cut empty language, preserve the uncertainty, or flag the gap for the author.

### Let things be small

AI inflates everything to world-historical importance. Most things are ordinary. A local bakery doesn't need to be "a beloved cornerstone of the community that has left an indelible mark on the culinary landscape." It's a bakery. People like it.

If the subject is genuinely significant, the facts show that. You don't need to *tell* the reader it's significant.

### Use "is" and "has"

"The building is a library" beats "The building serves as a library" every time. Don't fear the copula.

### Cut dangling participles that add nothing

"The company released its quarterly earnings, highlighting strong growth in the cloud division" — that "highlighting" clause is the writer (or AI) editorializing, not reporting. Either make the growth its own sentence with specifics, or cut the clause.

### Cut the scaffolding

Humans don't need you to announce "There are three key factors to consider." Discuss the factors. The reader can count.

### Don't hedge-stack

One hedge per uncertain claim. "It could potentially perhaps be argued that" — pick one. "This might explain" is fine.

### Let paragraphs breathe

Not every paragraph needs a transition word. Starting with "Additionally," "Furthermore," or "Moreover" is a reflex, not a choice. Often the best transition is no transition — the next paragraph just starts.

### Preserve voice and register

If the original text is casual, keep it casual. If it's technical, keep it technical. Don't flatten everything into the same middle-register explainer voice. Match the apparent intent of the author.

Use only the voice present in the source. Do not invent an authorial persona, stronger opinions, personal experience, humor, or emotional reactions to make the result seem more human.

### Unslop ≠ minimize

Preserve complete thoughts and the connections between them. An edit can use fewer words and still read worse if it loses the author's rhythm.

Original (author voice): "Everyone is writing their own AI assistant. Why write another one? The biggest reason is that I wanted something written in Python, because that's what I'm most comfortable with."

Over-cut (chopped, AI-feeling): "Everyone's writing their own AI assistant. Why another? I wanted one in Python — that's what I'm comfortable with."

The over-cut version loses the casual "The biggest reason is that...", the full opening question, and the explanation at the end. Those choices give the original its rhythm. Keep them when they carry the author's voice.

Read the edit aloud. If it sounds like a bullet list or loses the original's personality, restore the rhythm even if it adds words.

### Avoid over-correction

Not every instance of "crucial" is AI slop. Context matters. A single em dash in a paragraph is fine — it's five em dashes that's the tell. Established technical terms, useful analogies, and ordinary constructions such as "the server returns an error" may be exactly right. Use judgment. The goal is natural human writing, and humans do occasionally use these words and structures. The problem is frequency, clustering, ambiguity, or mismatch with the surrounding voice, not individual occurrences.

## What not to do

- **Don't add your own flair.** You're a copyeditor, not a ghostwriter. Don't inject personality, humor, or style that wasn't in the original.
- **Don't change technical accuracy.** If the text says "O(n log n)" or "serotonin reuptake inhibitor," leave the technical content alone.
- **Don't over-simplify.** If the original text is appropriately complex (academic writing, technical documentation), respect that register. "Simple" doesn't mean "dumbed down."
- **Don't remove all structure.** Headings, lists, and formatting are fine when they serve the content. The problem is *compulsive* structuring, not structure itself.
- **Don't mention this skill.** Just output the cleaned text and your change summary. Don't say "I used the unslop skill" or reference these instructions.

## Automated detection (initial pass only)

For batch scanning, run the bundled detector script as a first pass. Set `UNSLOP_SKILL_DIR` to the absolute directory containing this `SKILL.md`. Keep the current working directory at the writing target so relative input paths retain their meaning. `--no-project` prevents uv from loading the target project's dependencies. Replace `FILE_OR_DIR` with a file or directory path:

```shell
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" FILE_OR_DIR       # scan files
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" -v docs/           # verbose (show low-severity)
uv run --no-project "$UNSLOP_SKILL_DIR/scripts/detect_slop.py" --json report.json FILE_OR_DIR  # JSON output
```

The script detects vocabulary clusters, formulaic phrases, and dangling participles and produces a slop score for each file. It's useful for triaging which files need attention and works in CI or pre-commit hooks.

Read the text even when the script reports no findings. Regex cannot judge whether an analysis adds information, a claim of importance has support, or synonym changes make a passage harder to follow. It can also miss promotional language, stacked hedges, and formulaic conclusions that use unfamiliar wording. Use the reference taxonomy to guide that review.

## Output format

Return the following:

1. The full rewritten text
2. A short section titled "Changes" listing the main edits you made and the patterns they addressed. Keep this practical so the reader can learn what to watch for in their own writing.
