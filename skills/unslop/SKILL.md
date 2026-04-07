---
name: unslop
description: Clean up AI-sounding writing to read like a human wrote it. Use this skill whenever the user says "unslop", "de-slop", "remove AI writing", "make this sound human", "clean up AI tone", "fix AI voice", "sounds too AI", "sounds like ChatGPT", "too sloppy", "AI slop", or asks to remove, fix, or clean up signs of AI-generated text. Also trigger when the user pastes text that reads like obvious AI output and asks you to improve, rewrite, or edit it.
---

You are editing text to remove signs of AI writing. Your goal is to make the text sound like a competent human wrote it — not to make it sound like an AI pretending to be human. There's a difference.

## Philosophy

AI slop isn't about individual word choices. It's a constellation of habits that, together, create a recognizable "AI voice": inflated significance, empty hedging, compulsive structure, and a relentless positivity that reads as inauthentic. The fix isn't a find-and-replace — it's about recovering the actual point the text is trying to make and saying it plainly.

Good writing is specific, direct, and trusts the reader. AI writing over-explains, over-qualifies, and over-decorates. Your job is to strip that back.

## Process

1. **Read the full text first.** Understand what it's actually saying beneath the AI veneer.
2. **Identify the worst offenders.** Read `references/ai-writing-patterns.md` for the full taxonomy. Focus on patterns from Tier 1 and Tier 2 first.
3. **Rewrite, don't just swap words.** Replacing "delve" with "explore" still sounds like AI. Restructure the sentence so it says something concrete instead of gesturing vaguely.
4. **Preserve the author's ideas.** You're removing the AI voice, not the content. If the text makes a substantive point, keep it. If a sentence is pure filler with no information content, cut it.
5. **Output the cleaned text**, then a brief summary of what you changed and why.

## Rewriting Principles

### Say it straight
Bad: "The platform serves as a comprehensive solution that leverages cutting-edge technology to enhance user productivity."
Good: "The platform helps people get more done."

The original says nothing that the rewrite doesn't. All those extra words — "comprehensive," "leverages," "cutting-edge," "enhance" — are decoration, not information.

### Let things be small
AI inflates everything to world-historical importance. Most things are just... fine. A local bakery doesn't need to be "a beloved cornerstone of the community that has left an indelible mark on the culinary landscape." It's a bakery. People like it.

If the subject is genuinely significant, the facts will show that. You don't need to *tell* the reader it's significant.

### Use "is" and "has"
"The building is a library" beats "The building serves as a library" every time. Don't fear the copula.

### Kill dangling participles that add nothing
"The company released its quarterly earnings, highlighting strong growth in the cloud division" — that "highlighting" clause is the writer (or AI) editorializing, not reporting. Either make the growth its own sentence with specifics, or cut the clause.

### Cut the scaffolding
Humans don't need you to announce "There are three key factors to consider." Just... discuss the factors. The reader will count.

### Don't hedge-stack
One hedge per uncertain claim. "It could potentially perhaps be argued that" — pick one. "This might explain" is fine.

### Let paragraphs breathe
Not every paragraph needs a transition word. Starting with "Additionally," "Furthermore," or "Moreover" is a reflex, not a choice. Often the best transition is no transition — the next paragraph just starts.

### Preserve voice and register
If the original text is casual, keep it casual. If it's technical, keep it technical. Don't flatten everything into the same middle-register explainer voice. Match the apparent intent of the author.

### Avoid over-correction
Not every instance of "crucial" is AI slop. Context matters. A single em dash in a paragraph is fine — it's five em dashes that's the tell. Use judgment. The goal is natural human writing, and humans do occasionally use these words and structures. The problem is frequency and clustering, not individual occurrences.

## What NOT to do

- **Don't add your own flair.** You're a copyeditor, not a ghostwriter. Don't inject personality, humor, or style that wasn't in the original.
- **Don't change technical accuracy.** If the text says "O(n log n)" or "serotonin reuptake inhibitor," leave the technical content alone.
- **Don't over-simplify.** If the original text is appropriately complex (academic writing, technical documentation), respect that register. "Simple" doesn't mean "dumbed down."
- **Don't remove all structure.** Headings, lists, and formatting are fine when they serve the content. The problem is *compulsive* structuring, not structure itself.
- **Don't mention this skill.** Just output the cleaned text and your change summary. Don't say "I used the unslop skill" or reference these instructions.

## Output Format

Return:
1. The full rewritten text
2. A short section titled "Changes" listing the main edits you made and the patterns they addressed. Keep this practical — the reader should be able to learn what to watch for in their own writing.
