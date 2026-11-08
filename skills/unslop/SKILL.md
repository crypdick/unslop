---
name: unslop
description: Edit prose described as AI-sounding or ChatGPT-like. Use for requests to unslop, de-slop, remove AI tone, or make text sound human.
---

Remove formulaic phrasing and empty language while preserving the author's meaning, voice, register, and technical accuracy.

## Choose the target

Edit the supplied text, file, or directory.

Without a target, use [the detector](references/detector.md) to scan the current directory. Show ranked candidates and confirm scope unless already authorized. If no prose files or findings turn up, ask for a target.

## Editorial judgment

Read the full text for context. Rewrite for clarity rather than swapping flagged words. Consult [the taxonomy](references/ai-writing-patterns.md) as needed: prioritize Tier 1 and Tier 2; treat Tier 3 as contextual cues, not bans. Patterns do not prove AI authorship.

- Cut filler, inflated significance, and unnecessary scaffolding. Keep substantive ideas and explanations that add information.
- Remove caveats about invented objections; retain limits that affect attribution, evidence, or decisions.
- Preserve facts and accurate uncertainty. Name actors or mechanisms only when supported; do not invent details, opinions, or personality.
- Keep useful structure, technical terms, appropriate complexity, and explanatory analogies. Isolated words or punctuation do not justify edits.
- Preserve complete thoughts and natural rhythm. Brevity is not the goal when cutting flattens the author's voice.

Check the final edit for changed claims, lost meaning, and over-correction.

## Output

Return the full cleaned text followed by a brief **Changes** summary. For authorized file edits, also update files in place. Omit intermediate drafts and references to this skill.
