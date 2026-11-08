# AI writing patterns reference

Use these patterns to find passages worth editing, not to establish AI authorship.
Tiers indicate review priority. Judge information value and fit with the author's
voice; preserve useful detail, accurate uncertainty, and supported claims.
Isolated words or stylistic choices are not grounds for edits.

## Tier 1: high-priority patterns

### AI vocabulary clusters

Clusters such as "delve," "tapestry," "pivotal," "robust," "leverage," "paradigm,"
and "holistic" can replace precise description. Claims such as "groundbreaking"
need factual support.

### Copulative avoidance

Prefer "is" or "has" when "serves as," "stands as," or "boasts" adds no distinction.

### Formulaic significance framing

"Is a testament to" and "underscores the importance of" often assert significance
without explaining it. State the supported relationship.

### The "not just X, but Y" construction

Repeated "not just X, but Y" contrasts can inflate a simple point. State the point directly unless the contrast matters.

## Tier 2: recurring content problems

### Promotional/breathless tone

Replace empty promotion such as "commitment to excellence" with supported facts,
without removing the author's enthusiasm.

### Defensive caveats and invented objections

Cut denials of irrelevant alternatives. Keep qualifications that bound evidence, change attribution or decisions, or correct a plausible misunderstanding.

"The grader parsed zero of 45 passing tests. This was a parser incompatibility, not a model failure." can become "The grader's parser misread the output and extracted zero of 45 passing tests."

Removing a caveat must not broaden the claim beyond its evidence.

### Dangling present participle phrases

Trailing commentary such as "highlighting the need for further research" may add
nothing. Distinguish filler from concrete consequences.

### Rule of three abuse

Triplets such as "innovative, dynamic, and forward-thinking" can impose a template
without adding information. Meaningful groups of three are fine.

### Elegant variation (synonym cycling)

Cycling through "the researcher," "the scholar," and "the protagonist" can obscure
a single referent. Repeat the precise name or term when clearer.

### Vague attribution

"Experts argue" and "studies have shown" imply unidentified authority. Use only
supported attribution; do not invent citations or turn attributed claims into facts.

### Formulaic challenges/outlook conclusions

Replace generic optimism such as "While challenges remain, the future looks
promising" with concrete conclusions, unresolved problems, or next steps.

### False ranges

"From the Big Bang to dark matter" lacks a meaningful scale. List the topics or
explain their relationship; keep genuine intervals and scope boundaries.

### Excessive detail and over-explaining

Cut repetition, obvious explanations, and examples that add no useful distinction.
Keep detail needed by the audience or for correctness.

## Tier 3: contextual style cues

These warrant edits when they create repetition, ambiguity, or a mismatch with
voice—not merely because they occur.

### Decorative punctuation

Dashes, dramatic colons, and fragments can force emphasis: "Clear. Direct.
Transformative." Keep punctuation that clarifies meaning or fits the rhythm.

### Decorative compression

Labels such as "an insight-first workflow" or "the alignment loop" may substitute for explanation. State the literal action when clearer; keep established terms and authorial wording that carries meaning.

### Manufactured sentence rhythm

Runs of clipped fragments or over-packed clauses can sound mechanical. Split or join sentences to restore reasoning and rhythm, without imposing length or clause-count limits.

### Pseudo-agency

"The framework drives alignment" can hide who does what. Name supported actors
or mechanisms; conventional subjects such as "the server returns an error" are fine.

### Unexplained or invented jargon

Prefer plain language when more precise or accessible to the audience. Keep
established technical terms and appropriate complexity.

### Decorative analogies

Cut imagery that repeats an explanation; keep analogies that clarify a difficult
relationship or carry the author's voice.

### Ambiguous references

Clarify "this" or "the outcome" when several antecedents are plausible.

### Stacked rhetorical questions

Repeated questions can manufacture drama. State the issue directly unless an
answer is invited or the question structure helps the reader.

### Collaborative/direct address

"Let's explore" and "Here's why that matters" can delay the point. Keep direct
address that serves the relationship with the reader.

### Hedge stacking

Reduce redundant uncertainty such as "It could potentially be argued that
perhaps" without changing confidence.

### Transition word overuse

Keep transitions that express relationships, not repeated "Additionally" or
"Moreover" scaffolding.

### Filler phrases that add nothing

Cut empty prefaces such as "It's worth noting that" and "When it comes to."

### Formulaic scaffolding and paragraph structure

Announcements such as "There are three key aspects" and repeated announcement-support-summary paragraphs can delay content. Keep topic sentences, counts, and structure that help navigation.

### Inline-header vertical lists

Remove redundant labels such as "**Performance:** Performance improved...";
keep useful parallel lists.

### Decorative emoji

Remove mechanical decoration such as "🚀 Launch" when it carries no meaning. Preserve authorial style, brand conventions, and status indicators.

### Title case overuse in headings

Match the document's heading style.

### Sycophantic/validating opener

Cut reflexive praise such as "Great question!" when it delays content.

### Pasted chatbot artifacts

Remove wrappers such as "I hope this helps" from standalone prose, not genuine
correspondence.

### Knowledge-cutoff disclaimers

Replace model-specific framing such as "Up to my last training update" with source-specific uncertainty when relevant. Verify, preserve, or flag an honest gap; never fill it with a guess.

### Curly/smart quotes

Match the target's typography; curly quotes alone need no rewrite.

### Excessive boldface

Remove redundant emphasis; keep boldface that helps scanning or follows convention.

### Notability/media coverage emphasis

"Garnered widespread media attention" or lists of publications can imply importance without supporting it. Keep coverage facts relevant to the point; cut inflated conclusions.

### Sudden shifts in writing style

Check abrupt tone or complexity changes against context; quotations or audience
changes may justify them.

## Detection guardrails

Preserve wording in quotations, titles, code, and examples when it is being
discussed rather than used. Automated detection supplies triage cues, not judgments
about clarity, usefulness, or voice. A clean scan does not establish good prose.
