"""Regular expressions and vocabulary for the writing-pattern taxonomy."""

import re

# NOTE: Keep README.md "What it catches" and skills/unslop/references/ai-writing-patterns.md aligned.
# Tier 1: Dead giveaways when clustered
AI_VOCABULARY = {
    # Classic LLM lexicon
    "delve",
    "tapestry",
    "pivotal",
    "crucial",
    "underscore",
    "vibrant",
    "meticulous",
    "intricate",
    "intricacies",
    "testament",
    "garner",
    "bolstered",
    "fostering",
    "showcasing",
    "highlighting",
    "emphasizing",
    "enduring",
    "nuanced",
    "multifaceted",
    "comprehensive",
    "robust",
    "leverage",
    "realm",
    "paradigm",
    "cornerstone",
    "beacon",
    "spearhead",
    "demystify",
    "unpack",
    "harness",
    "catalyze",
    "synergy",
    "holistic",
    "granular",
    "unravel",
    "interplay",
    # Inflation words
    "groundbreaking",
    "revolutionary",
    "transformative",
    "game-changing",
    "unprecedented",
    "invaluable",
    "indispensable",
    "indelible",
    # Promotional
    "renowned",
    "exemplifies",
}

# Words that are only AI-ish when used metaphorically (need context)
CONTEXT_DEPENDENT = {"landscape", "navigate", "deep dive", "enhance"}

# Formulaic phrases — regex patterns with display names
FORMULAIC_PHRASES = [
    # Significance inflation
    (r"\bis a testament to\b", "significance inflation: 'is a testament to'"),
    (r"\bstands as a\b", "copulative avoidance: 'stands as a'"),
    (r"\bserves as a\b", "copulative avoidance: 'serves as a'"),
    (
        r"\bplays a (?:vital|crucial|pivotal|key) role\b",
        "significance inflation: 'plays a [vital/crucial/pivotal] role'",
    ),
    (r"\bunderscores the importance\b", "significance inflation: 'underscores the importance'"),
    (r"\breflects? broader\b", "significance inflation: 'reflects broader'"),
    (r"\bsetting the stage for\b", "significance inflation: 'setting the stage for'"),
    (r"\bkey turning point\b", "significance inflation: 'key turning point'"),
    (r"\bindelible mark\b", "significance inflation: 'indelible mark'"),
    (r"\bevolving landscape\b", "significance inflation: 'evolving landscape'"),
    (r"\bat the intersection of\b", "significance inflation: 'at the intersection of'"),
    (
        r"\bin today'?s (?:rapidly )?(?:evolving|changing|digital)\b",
        "formulaic opener: 'in today's rapidly evolving...'",
    ),
    # "Not just X but Y"
    (r"\bnot just\b.{1,40}\bbut (?:also|a)\b", "'not just X, but also Y' construction"),
    (r"\bmore than just\b", "'more than just' construction"),
    (r"\bisn'?t merely\b", "'isn't merely' construction"),
    # Promotional
    (r"\bboasts a\b", "promotional: 'boasts a'"),
    (r"\brich tapestry\b", "promotional: 'rich tapestry'"),
    (r"\bnestled in the heart of\b", "promotional: 'nestled in the heart of'"),
    (r"\bdiverse array\b", "promotional: 'diverse array'"),
    (
        r"\bcommitment to (?:excellence|innovation|quality)\b",
        "promotional: 'commitment to excellence/innovation'",
    ),
    # Vague attribution
    (r"\bexperts (?:argue|suggest|believe|note)\b", "vague attribution: 'experts argue/suggest'"),
    (r"\bindustry reports (?:suggest|indicate|show)\b", "vague attribution: 'industry reports suggest'"),
    (r"\bit is widely (?:recognized|known|accepted)\b", "vague attribution: 'it is widely recognized'"),
    (r"\bstudies have shown\b", "vague attribution: 'studies have shown'"),
    # Formulaic conclusions
    (
        r"\bdespite (?:its|these|the) .{1,30}(?:challenges|limitations)\b",
        "formulaic conclusion: 'despite its... challenges'",
    ),
    (r"\bas \w+ continues? to evolve\b", "formulaic conclusion: 'as X continues to evolve'"),
    (r"\bmoving forward\b", "formulaic conclusion: 'moving forward'"),
    (r"\bonly time will tell\b", "formulaic conclusion: 'only time will tell'"),
    # Filler phrases
    (r"\bit'?s worth noting that\b", "filler: 'it's worth noting that'"),
    (r"\bit'?s important to (?:remember|note|recognize)\b", "filler: 'it's important to remember'"),
    (r"\bit goes without saying\b", "filler: 'it goes without saying'"),
    (r"\bat the end of the day\b", "filler: 'at the end of the day'"),
    (r"\bwhen it comes to\b", "filler: 'when it comes to'"),
    (r"\bthe reality is that\b", "filler: 'the reality is that'"),
    # Collaborative address
    (
        r"\blet'?s (?:delve|dive|unpack|explore|examine)\b",
        "collaborative address: 'let's delve/dive/explore'",
    ),
    (r"\bas we'?ll see\b", "collaborative address: 'as we'll see'"),
    (r"\bhere'?s (?:the thing|why)\b", "collaborative address: 'here's the thing/why'"),
    # Sycophantic openers
    (r"^(?:Great|Excellent|Fantastic|Wonderful) (?:question|point|observation)\b", "sycophantic opener"),
    (r"^(?:Absolutely|Exactly)[!.]", "sycophantic opener"),
    (
        r"^You raise a (?:really |very )?(?:important|great|excellent|good) (?:point|issue|question)\b",
        "sycophantic opener",
    ),
    # Structural scaffolding
    (
        r"\bthere are (?:three|four|five|several|many|a number of) (?:key|main|important|critical|primary) ",
        "structural scaffolding: 'there are N key...'",
    ),
    (r"\blet'?s break (?:this|it) down\b", "structural scaffolding: 'let's break this down'"),
    # Notability emphasis
    (r"\b(?:renowned|acclaimed|celebrated) (?:for|as)\b", "notability emphasis: 'renowned/acclaimed for'"),
    (r"\bwidely regarded as\b", "notability emphasis: 'widely regarded as'"),
]

# Dangling present participle fillers (end-of-sentence)
DANGLING_PARTICIPLE_RE = re.compile(
    r",\s*(?:thereby\s+)?"
    r"(?:highlighting|underscoring|emphasizing|showcasing|reflecting|"
    r"demonstrating|illustrating|reinforcing|fostering|ensuring|"
    r"contributing to|paving the way for|signaling|solidifying)"
    r"\b[^.!?]*[.!?]",
    re.IGNORECASE,
)

# Compile formulaic patterns
COMPILED_PHRASES = [(re.compile(p, re.IGNORECASE), name) for p, name in FORMULAIC_PHRASES]

# Pasted assistant correspondence that does not belong in standalone prose.
CHATBOT_ARTIFACT_PATTERNS = [
    (r"\bi hope this helps[.!]?", "chatbot residue: 'I hope this helps'"),
    (
        r"\blet me know if you(?:['\u2019]d| would) like\b",
        "chatbot residue: 'let me know if you'd like'",
    ),
    (r"\bwould you like me to\b", "chatbot residue: 'would you like me to'"),
    (
        r"\bas an ai (?:language )?(?:model|assistant)\b",
        "chatbot residue: 'as an AI model'",
    ),
]
COMPILED_CHATBOT_ARTIFACTS = [
    (re.compile(pattern, re.IGNORECASE), message) for pattern, message in CHATBOT_ARTIFACT_PATTERNS
]

# Explicit model-knowledge disclaimers that often leak from chat into content.
# These are deliberately narrower than generic uncertainty phrases: honest
# uncertainty is not slop; the editor must preserve it without guessing.
KNOWLEDGE_CUTOFF_PATTERNS = [
    (
        r"\b(?:up to|as of) my last (?:knowledge|training) (?:update|cutoff)\b",
        "knowledge-cutoff disclaimer: 'up to my last ... update'",
    ),
    (
        r"\bmy (?:knowledge|training) cutoff (?:is|was)\b",
        "knowledge-cutoff disclaimer: 'my knowledge cutoff is'",
    ),
    (
        (
            r"\bi don['\u2019]?t have access to (?:real[- ]time|current) "
            r"(?:data|information)\b"
        ),
        "knowledge-cutoff disclaimer: no access to current information",
    ),
]
COMPILED_KNOWLEDGE_CUTOFFS = [
    (re.compile(pattern, re.IGNORECASE), message) for pattern, message in KNOWLEDGE_CUTOFF_PATTERNS
]

# Transition words that AI overuses at sentence starts
TRANSITION_STARTERS = re.compile(
    r"^(?:Additionally|Furthermore|Moreover|Importantly|Notably|"
    r"Interestingly|That said|Nevertheless|Consequently|Subsequently|"
    r"Ultimately|Essentially|Fundamentally)[,:]?\s",
    re.MULTILINE,
)

# Rule of three: "adjective, adjective, and adjective" pattern
RULE_OF_THREE_RE = re.compile(
    r"\b(\w+), (\w+),? and (\w+)\b",
    re.IGNORECASE,
)

# Title case heading detection (markdown headings)
TITLE_CASE_HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)

# Curly/smart quotes and apostrophes
CURLY_QUOTES_RE = re.compile(r"[\u2018\u2019\u201C\u201D]")

# Markdown bold overuse
BOLD_RE = re.compile(r"\*\*[^*]+\*\*")

# Em dash (for density check)
EM_DASH_RE = re.compile(r"\u2014|--")

# Repeated list items with mechanical bold labels, such as
# "- **Performance:** Performance improved." One item can be useful; a run of
# them is the stronger stylistic signal.
INLINE_HEADER_ITEM_RE = re.compile(
    r"^\s*(?:[-*+]|\d+[.)])\s+\*\*[^*\n]{1,60}:\*\*",
    re.MULTILINE,
)

# Decorative emoji at the beginning of headings or list items. Restrict the
# check to line-leading decoration to avoid flagging ordinary emoji in prose.
DECORATIVE_EMOJI_LINE_RE = re.compile(
    r"^\s*(?:(?:#{1,6}|[-*+])\s+)?"
    r"[\U0001F300-\U0001FAFF\u2600-\u27BF]",
    re.MULTILINE,
)
