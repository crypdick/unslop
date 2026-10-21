---
name: unslop
description: Edit AI-sounding prose to preserve meaning and voice. Use for unslop, de-slop, removing AI writing or tone, making text sound human, or rewriting text described as sounding like ChatGPT.
---

Edit AI-sounding text while preserving the author's meaning, voice, register, and technical accuracy.

## Choose the target

If the user supplied text, a file, or a directory, edit that target.

For an invocation without arguments or pasted text, scan the current working directory using [the detector workflow](references/detector.md). Show ranked candidates and confirm editing scope unless the user already authorized it. Ask for a target only if there are no candidate prose files or findings.

## Edit

1. Read the full text to understand its point and voice.
2. Identify inflated significance, empty hedges, vague abstractions, formulaic phrasing, unnecessary structure, and forced positivity. For pattern definitions and examples, consult [the taxonomy](references/ai-writing-patterns.md). Prioritize Tier 1 and Tier 2; treat Tier 3 as contextual review cues.
3. Rewrite sentences rather than swapping flagged words. Cut filler; retain substantive ideas, facts, useful structure, and accurate uncertainty. Name actors and mechanisms only when supported by the source.
4. Draft privately, then audit for remaining patterns, changed claims, invented details, and flattened rhythm. Inspect Tier 3 patterns when they cluster, repeat, obscure meaning, or clash with the voice. Read aloud mentally and revise mechanical terseness.

## Preserve meaning and rhythm

- Prefer direct verbs and concrete relationships. Remove redundant transitions, significance claims, and dangling commentary; keep explanations that add information.
- Cut defensive caveats that answer invented objections. Keep limits that affect attribution, evidence, or decisions; see [the taxonomy](references/ai-writing-patterns.md#defensive-caveats-and-invented-objections).
- Keep technical terms, appropriate complexity, useful analogies, and the author's register. A watched word, em dash, or three-item list alone is not a reason to edit.
- Do not add opinions, humor, personal experience, or personality absent from the source. Do not invent facts to replace uncertainty.
- Keep headings and lists when they help the reader. Cut compulsory scaffolding and decorative formatting, not useful structure.
- Keep function words and conjunctions that connect complete thoughts. Shorter prose can read worse if it loses the author's rhythm.

Original: "Everyone is writing their own AI assistant. Why write another one? The biggest reason is that I wanted something written in Python, because that's what I'm most comfortable with."

Over-cut: "Everyone's writing their own AI assistant. Why another? I wanted one in Python — that's what I'm comfortable with."

The full question and casual explanation carry voice. Restore them when cutting makes the edit sound like a bullet list.

## Output

Return the full final cleaned text, followed by a brief **Changes** section explaining the main edits and patterns addressed. For authorized file edits, also update files in place. Do not show intermediate drafts or mention the skill.
