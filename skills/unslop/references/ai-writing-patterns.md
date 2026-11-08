# AI writing patterns reference

Use these patterns to find passages worth editing, not to establish AI authorship. Judge repetition, information value, and fit with the author's voice. Tiers indicate review priority, not certainty.

## Tier 1: high-priority patterns

### AI vocabulary clusters

Clusters of stock language can replace precise description: "delve," "tapestry," "pivotal," "robust," "leverage," "paradigm," or "holistic." Inflation words such as "groundbreaking," "transformative," and "unprecedented" need factual support. Individual words are not grounds for an edit.

### Copulative avoidance

Prefer "is" or "has" when phrases such as "serves as," "stands as," or "boasts" add no meaning. Keep alternatives that express a real distinction.

### Formulaic significance framing

Phrases such as "is a testament to," "plays a pivotal role," and "underscores the importance of" can assert significance without explaining it. Keep the supported relationship; cut empty promotion.

### The "not just X, but Y" construction

Repeated "not just X, but Y" contrasts can inflate a simple point. State the point directly unless the contrast matters.

## Tier 2: recurring content problems

### Promotional/breathless tone

Replace press-release language such as "boasts a vibrant," "rich tapestry," or "commitment to excellence" with supported facts. Preserve enthusiasm that belongs to the author.

### Defensive caveats and invented objections

Cut denials of irrelevant alternatives. Keep qualifications that bound evidence, change attribution or decisions, or correct a plausible misunderstanding.

"The grader parsed zero of 45 passing tests. This was a parser incompatibility, not a model failure." can become "The grader's parser misread the output and extracted zero of 45 passing tests."

Removing a caveat must not broaden the claim beyond its evidence.

### Dangling present participle phrases

Trailing clauses such as "highlighting the need for further research" or "fostering a sense of community" may add only commentary. Cut them when empty; retain concrete consequences.

### Rule of three abuse

Repeated triplets such as "innovative, dynamic, and forward-thinking" can impose a template instead of adding information. Keep meaningful groups of three.

### Elegant variation (synonym cycling)

Cycling through "the researcher," "the scholar," and "the protagonist" can obscure a single referent. Repeat the precise name or term when clearer.

### Vague attribution

"Experts argue" and "studies have shown" suggest authority without identifying it. Use attribution supported by the source; do not invent a citation or turn an attributed claim into an established fact.

### Formulaic challenges/outlook conclusions

Cut generic endings such as "While challenges remain, the future looks promising" when they add no conclusion. Keep concrete unresolved problems and next steps.

### False ranges

"From the Big Bang to dark matter" presents topics as endpoints without a meaningful scale. List the topics or explain their relationship. Keep genuine intervals, progressions, and scope boundaries.

### Excessive detail and over-explaining

Cut repeated instructions, obvious explanations, and examples that add no useful distinction. "Define every variable in an equation" may suffice without enumerating symbols, subscripts, and superscripts. Keep detail needed by the audience or for correctness.

## Tier 3: contextual style cues

Edit these when repetition, ambiguity, or mismatch with the voice creates a problem. They are not prohibited constructions.

### Decorative punctuation

Repeated dashes, dramatic colons, and fragments can force emphasis: "Clear. Direct. Transformative." Keep punctuation that clarifies meaning or fits the author's rhythm.

### Decorative compression

Labels such as "an insight-first workflow" or "the alignment loop" may substitute for explanation. State the literal action when clearer; keep established terms and authorial wording that carries meaning.

### Manufactured sentence rhythm

Runs of clipped fragments or over-packed clauses can sound mechanical. Split or join sentences to restore reasoning and rhythm, without imposing length or clause-count limits.

### Pseudo-agency

"The framework drives alignment" can hide who does what. Name supported actors or mechanisms. Conventional subjects such as "the server returns an error" and "the paper argues" are fine.

### Unexplained or invented jargon

Replace jargon that is less precise than plain language or unexplained for the intended audience. Keep established technical terms and appropriate complexity.

### Decorative analogies

Cut imagery that merely repeats a clear explanation. Keep analogies that explain a difficult relationship or carry the author's voice.

### Ambiguous references

Clarify "this," "the result," or "the outcome" when several antecedents are plausible. Leave clear references alone.

### Stacked rhetorical questions

Repeated questions can manufacture drama. State the issue directly when no answer is invited; keep genuine questions and useful interview or FAQ structure.

### Collaborative/direct address

"Let's explore," "As we'll see," and "Here's why that matters" can delay the point. Keep direct address when it serves the relationship with the reader.

### Hedge stacking

Reduce redundant uncertainty such as "It could potentially be argued that perhaps." Preserve the actual degree of confidence.

### Transition word overuse

Repeated "Additionally," "Moreover," and "Notably" can become verbal scaffolding. Keep transitions that express a useful relationship.

### Filler phrases that add nothing

Cut empty prefaces such as "It's worth noting that," "At the end of the day," and "When it comes to."

### Formulaic scaffolding and paragraph structure

Announcements such as "There are three key aspects" and repeated announcement-support-summary paragraphs can delay content. Keep topic sentences, counts, and structure that help navigation.

### Inline-header vertical lists

Repeated labels such as "**Performance:** Performance improved..." can make prose harder to scan. Remove redundant labels or combine points; retain useful parallel lists.

### Decorative emoji

Remove mechanical decoration such as "🚀 Launch" when it carries no meaning. Preserve authorial style, brand conventions, and status indicators.

### Title case overuse in headings

Match the document's heading style rather than imposing Title Case For Every Heading.

### Sycophantic/validating opener

Cut reflexive praise such as "Great question!" or "That's an excellent point!" when it delays the content.

### Pasted chatbot artifacts

Remove wrappers such as "I hope this helps" or "Let me know if you'd like more detail" from standalone prose. Keep genuine correspondence addressed to another person.

### Knowledge-cutoff disclaimers

Replace model-specific framing such as "Up to my last training update" with source-specific uncertainty when relevant. Verify, preserve, or flag an honest gap; never fill it with a guess.

### Curly/smart quotes

Match the target's typography. Curly quotes alone do not justify rewriting prose.

### Excessive boldface

Remove repetitive emphasis that the prose can carry. Keep boldface that helps readers scan or follows an established convention.

### Notability/media coverage emphasis

"Garnered widespread media attention" or lists of publications can imply importance without supporting it. Keep coverage facts relevant to the point; cut inflated conclusions.

### Sudden shifts in writing style

Check abrupt changes in tone or complexity against the surrounding voice. Preserve justified shifts, such as quotations or changes of audience.

## Detection guardrails

Do not rewrite watched phrases inside quotations, titles, code, or examples where the wording is being discussed rather than used. Keep judgments about clarity, usefulness, and voice out of automated detection; regex findings are triage cues, and clean scans do not establish good prose.
