# AI Writing Patterns Reference

Taxonomy of AI writing tells, drawn from Wikipedia's "Signs of AI writing" and first-hand observation. Organized by severity and detectability.

## Tier 1: Dead Giveaways (almost never appear in natural human writing)

### AI Vocabulary Clusters

When multiple words from this list appear in close proximity, it's a strong signal. One or two in isolation can be human; three or more clustered together almost never is.

**The classic LLM lexicon:**
delve, tapestry, landscape (metaphorical), pivotal, crucial, underscore, vibrant, meticulous, intricate, testament, garner, bolstered, fostering, showcasing, highlighting, emphasizing, enhance, enduring, nuanced, multifaceted, comprehensive, robust, leverage, realm, paradigm, cornerstone, beacon, spearhead, demystify, unpack, navigate (metaphorical), harness, catalyze, synergy, holistic, granular, deep dive, unravel

**Inflation words (make everything sound world-historically important):**
groundbreaking, revolutionary, transformative, game-changing, unprecedented, remarkable, extraordinary, invaluable, indispensable, indelible

### Copulative Avoidance

AI models systematically replace "is" and "are" with fancier alternatives, even when the simple form is clearly better:
- "serves as" instead of "is"
- "stands as" instead of "is"
- "represents" instead of "is"
- "marks" instead of "is"
- "boasts" instead of "has"
- "features" instead of "has"
- "offers" instead of "has"

### Formulaic Significance Framing

Connecting mundane things to grand narratives:
- "is a testament to..."
- "plays a vital/crucial/pivotal role in..."
- "underscores the importance of..."
- "reflects broader trends in..."
- "setting the stage for..."
- "marks a key turning point"
- "left an indelible mark on..."
- "in the evolving landscape of..."
- "at the intersection of X and Y"

### The "Not Just X, But Y" Construction

Almost pathognomonic of AI writing:
- "It's not just about X; it's about Y"
- "This isn't merely X — it's Y"
- "More than just X, it represents Y"

---

## Tier 2: Strong Signals (humans do these sometimes, AI does them constantly)

### Promotional/Breathless Tone

Even when asked to be neutral, AI defaults to press-release voice:
- "boasts a vibrant..."
- "rich tapestry of..."
- "nestled in the heart of..."
- "a diverse array of..."
- "showcasing the best of..."
- "a testament to the power of..."
- "commitment to excellence/innovation/quality"
- "natural beauty"
- "renowned for its..."

### Dangling Present Participle Phrases

AI loves appending "-ing" clauses to the end of sentences for superficial depth:
- "...highlighting the need for further research"
- "...underscoring the importance of X"
- "...emphasizing the role of Y"
- "...reflecting broader societal trends"
- "...contributing to a more inclusive environment"
- "...fostering a sense of community"
- "...ensuring that all stakeholders are aligned"

These almost always add zero information — they're filler that gestures at significance without earning it.

### Rule of Three Abuse

Compulsive triplet structures:
- "innovative, dynamic, and forward-thinking"
- "clarity, precision, and depth"
- "research, analysis, and implementation"

Humans use the rule of three occasionally for rhetorical effect. AI uses it as a default structure for everything.

### Elegant Variation (Synonym Cycling)

Repetition penalties cause AI to cycle through synonyms instead of just repeating a word:
- A person becomes "the researcher," "the scholar," "the key figure," "the protagonist"
- A company becomes "the firm," "the organization," "the entity," "the tech giant"

Humans repeat words. It's fine. Forced variation reads as evasive.

### Vague Attribution

Claiming consensus or authority without specifics:
- "Experts argue that..."
- "Industry reports suggest..."
- "Observers have noted..."
- "Many researchers believe..."
- "Studies have shown..."
- "It is widely recognized that..."
- "According to several sources..."

### Formulaic Challenges/Outlook Conclusions

The AI essay coda:
- "Despite its [positive words], [subject] faces several challenges..."
- "While challenges remain, the future looks promising..."
- "As [subject] continues to evolve..."
- "Moving forward, it will be important to..."
- "Only time will tell whether..."

### False Ranges

LLMs use "from X to Y" as a dramatic container even when X and Y are not endpoints on a meaningful scale:
- "from the Big Bang to dark matter"
- "from strategy to empathy"
- "from individual choices to global transformation"

List the actual topics or state the relationship between them. Keep a range when the endpoints really do define an interval, progression, or scope.

---

## Tier 3: Stylistic Tells (subtler, but accumulate)

Tier 3 patterns are prompts to inspect the prose, not prohibited constructions. Rewrite them when they cluster, repeat, obscure the meaning, manufacture importance, or conflict with the surrounding voice. Preserve isolated uses that are clear, conventional, or characteristic of the author.

### Decorative Punctuation

AI often uses repeated em dashes, dramatic colons, and fragments to manufacture a reveal-and-punchline cadence:
- "The conclusion was clear: the framework had changed everything."
- "The next step — the one that really matters — is alignment."
- "Clear. Direct. Transformative."

Rewrite punctuation when it is doing rhetorical work that the content has not earned. Keep a dash, colon, or fragment when it is well placed and fits the author's voice. Density and repetition are the signal, not the mark itself.

### Decorative Compression

AI coins hyphenated labels, slogans, and metaphorical summaries to make ordinary ideas sound compact or memorable:
- "an insight-first workflow"
- "the alignment loop"
- "a reveal-style explanation"

Restate the literal action or relationship when the label substitutes for an explanation. Keep established terms and wording that the author already uses.

### Manufactured Sentence Rhythm

AI can produce runs of clipped fragments for emphasis or pack loosely related clauses into an over-controlled sentence. Both create prose that sounds assembled:
- "The edit is clear. Direct. Human. It lands."
- "The parser reads the file, the validator checks the fields, the writer saves the record, and the dashboard updates."

Split or join sentences when the rhythm obscures the reasoning or differs sharply from the surrounding prose. Do not enforce a sentence-length or clause-count limit.

### Pseudo-Agency

AI often makes abstractions sound like actors:
- "The strategy unlocks growth."
- "The framework drives alignment."
- "The result speaks to a broader shift."

Name the actor or mechanism when the construction hides it. Keep conventional technical or academic usage such as "the server returns an error" or "the paper argues."

### Unexplained or Invented Jargon

AI may invent compact terminology or use technical language to make a simple claim sound authoritative. Replace jargon when it is unnecessary, undefined for the intended audience, or less precise than ordinary language.

Keep established technical terms. A general dictionary is not the test; audience, precision, and context are.

### Decorative Analogies

AI analogies sometimes restate a simple idea with extra imagery instead of explaining it. Cut an analogy when the literal explanation already does the work.

Keep an analogy when it makes a difficult relationship easier to understand or clearly belongs to the author's voice.

### Ambiguous References

Words such as "this," "that," "the result," and "the outcome" become a problem when they could refer to several earlier ideas. Name the specific action or claim when the reference is unclear.

Do not mechanically replace every demonstrative pronoun or summary noun. Clear references are ordinary prose.

### Stacked Rhetorical Questions

Several rhetorical questions in a row can manufacture uncertainty or drama:
- "Does the rewrite preserve the voice? Does it keep the facts? Does it avoid over-correcting?"

State the issue directly when the questions do not invite answers. Keep real questions in interviews, FAQs, correspondence, or passages where the author is genuinely asking the reader to consider them.

### Collaborative/Direct Address

- "Let's explore..."
- "As we'll see..."
- "In this article, we'll examine..."
- "Let's dive in" / "Let's unpack this"
- "Here's the thing:"
- "Here's why that matters:"

### Hedge Stacking

Multiple hedges in one sentence:
- "It could potentially be argued that perhaps..."
- "While it may seem somewhat counterintuitive..."

### Transition Word Overuse

Starting every paragraph or sentence with:
- "Additionally," "Furthermore," "Moreover,"
- "Importantly," "Notably," "Interestingly,"
- "That said," "However," "Nevertheless,"

### Filler Phrases That Add Nothing

- "It's worth noting that..."
- "It's important to remember that..."
- "It goes without saying that..." (then says it)
- "At the end of the day..."
- "When it comes to..."
- "In terms of..."
- "The reality is that..."

### Formulaic Scaffolding and Paragraph Structure

Over-signposting:
- "First, ... Second, ... Third, ... Finally, ..."
- "There are three key aspects to consider:"
- "Two cautions."
- "Let's break this down into components:"

Repeated announcement-support-summary paragraphs can also make a document feel templated. Remove scaffolding or vary the structure when several paragraphs use the same mold. Keep topic sentences, explicit counts, and lists when they help readers navigate the material.

### Inline-Header Vertical Lists

Repeated bullets with bold labels often turn ordinary prose into a template:
- "**Performance:** Performance improved through optimization."
- "**Security:** Security was strengthened with encryption."
- "**Usability:** Usability was enhanced by the new interface."

Remove the repeated labels or combine the points when the list adds no scanability. Keep a list when the items are genuinely parallel and readers need to scan them.

### Decorative Emoji

Emoji attached mechanically to headings and bullets can make a document look like chatbot output:
- "🚀 **Launch:** Ship in Q3"
- "💡 **Insight:** Users prefer fewer steps"
- "✅ **Next step:** Schedule the review"

Remove decoration that carries no meaning. Keep emoji when it belongs to the author's established voice or communicates a real status convention.

### Title Case Overuse in Headings

AI defaults to Title Case For Every Heading even when the surrounding document uses sentence case.

### Sycophantic/Validating Opener

Starting responses with:
- "Great question!"
- "That's an excellent point."
- "Absolutely!"
- "You raise a really important issue."

### Pasted Chatbot Artifacts

Chat correspondence sometimes leaks into the document itself:
- "I hope this helps!"
- "Let me know if you'd like more detail."
- "Would you like me to continue?"
- "As an AI language model..."

Delete the conversational wrapper and begin with the content. Do not remove similar language from an actual email or message where the author is genuinely addressing another person.

### Knowledge-Cutoff Disclaimers

Model-specific disclaimers do not belong in standalone prose:
- "Up to my last training update..."
- "My knowledge cutoff is..."
- "I don't have access to real-time information..."

Rewrite the limitation as ordinary, source-specific uncertainty when it matters. Never replace an honest gap with a fabricated fact; verify it, preserve the uncertainty, or flag it for the author.

### Curly/Smart Quotes

AI often outputs curly quotes (\u2018\u2019\u201C\u201D) instead of straight ASCII quotes. This is a minor tell but correlates with AI origin, especially in plain-text contexts where smart quotes look out of place.

### Excessive Boldface

Mechanical, repetitive bolding — every instance of a key term, "key takeaways" formatting, or bolding entire phrases for emphasis that the prose should carry on its own.

### Notability/Media Coverage Emphasis

AI inflates coverage significance:
- "profiled in major publications"
- "garnered widespread media attention"
- "featured in leading industry outlets"
- "maintains a strong digital presence"

Often lists media sources to prove importance when the coverage is routine or trivial.

### Sudden Shifts in Writing Style

An abrupt change in tone, vocabulary level, or complexity mid-document. Often visible when AI-generated sections are interleaved with human writing, or when a prompt changed partway through generation.

---

## Detection Guardrails

These patterns are editing signals, not proof that AI wrote the text. Look for clusters, repetition, and mismatch with the surrounding voice.

- Do not rewrite watched phrases inside quotations, titles, code, or examples where the phrase is being discussed rather than used.
- Curly quotes, one em dash, one three-item list, or one emoji mean little on their own.
- A "from X to Y" range is fine when X and Y are comparable endpoints.
- Bold-label lists and emoji may be deliberate interface or brand conventions.
- Preserve established jargon, useful analogies, clear pronoun references, and conventional inanimate subjects.
- Prefer density or sequence checks over flagging one punctuation mark, question, modifier, or sentence shape.
- Keep patterns that require judging clarity, usefulness, or authorial voice out of automated detection.
- Preserve accurate uncertainty. Removing model-specific disclaimers does not authorize guessing.
