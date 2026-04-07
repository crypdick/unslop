# AI Writing Patterns Reference

Comprehensive taxonomy of AI writing tells, derived from Wikipedia's "Signs of AI writing" and general observation. Organized by severity and detectability.

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

---

## Tier 3: Stylistic Tells (subtler, but accumulate)

### Excessive Em Dashes

AI uses em dashes (—) far more frequently than most human writers, often multiple per paragraph.

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

### Excessive Structural Scaffolding

Over-signposting:
- "First, ... Second, ... Third, ... Finally, ..."
- "There are three key aspects to consider:"
- "Let's break this down into components:"

### Title Case Overuse in Headings

AI defaults to Title Case For Every Heading even when the surrounding document uses sentence case.

### Sycophantic/Validating Opener

Starting responses with:
- "Great question!"
- "That's an excellent point."
- "Absolutely!"
- "You raise a really important issue."

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
