---
name: unslop
description: Edit prose described as AI-sounding or ChatGPT-like. Use for requests to unslop, de-slop, remove AI tone, or make text sound human.
---

Remove formulaic phrasing and empty language while preserving meaning, voice,
register, and technical accuracy.

## Choose the target

Edit the supplied text, file, or directory. Without a target, use
[the detector](references/detector.md) in the current directory. Show ranked
candidates and confirm scope unless already authorized. If none turn up, ask for
a target.

## Editorial judgment

Read the full text for context and edit for clarity, not to satisfy a word blacklist. Consult
[the taxonomy](references/ai-writing-patterns.md) as needed; tiers indicate review
priority, not proof of AI authorship.

Cut filler, inflated claims, invented objections, and structure that adds no
information. Preserve substantive ideas, supported facts, accurate uncertainty,
and useful explanations. Retain caveats that affect evidence, attribution, or
decisions. Do not invent actors, evidence, opinions, or personality.

Keep technical terms, useful structure, explanatory analogies, and complete
thoughts. Brevity is not the goal when cutting flattens the author's voice or
reasoning. Change words, punctuation, or complexity only when they cause a real
problem. Check the result for changed claims, lost meaning, and over-correction.

## Output

Return the full cleaned text followed by a brief **Changes** summary. For
authorized file edits, also update files in place. Omit intermediate drafts and
references to this skill.
