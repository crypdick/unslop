---
name: taste-enforcer
enabled: true
event: prompt
pattern: don.?t use|always prefer|avoid|never do|instead of|I hate when|stop using|should always|should never|prefer .+ over|ban |forbid
action: warn
---

A keyword matched. The user might have expressed a coding preference or taste.

When the user expresses a coding preference that needs ongoing enforcement, determine which of these mechanisms can enforce it:

1. **A prek hook script:** Use a script for code patterns that static checks can detect, such as bare `except` clauses or print statements. Create or update a script in `scripts/prek_hooks/` and configure it in `prek.toml`.

2. **A hookify rule:** Use a rule for Claude's behavior during sessions, such as avoiding `utils.py` files or using `NewType` for IDs. Create a `.claude/hookify.{name}.md` rule, replacing `{name}` with a descriptive rule name.

3. **A `pyproject.toml` setting:** Use a setting for preferences that map to an existing tool's configuration, such as a Ruff rule that bans star imports.

If the preference is already enforced by an existing hook or rule but the user still had to say something about it, that means the existing enforcement failed to do its job. Identify why it didn't catch the issue (pattern too narrow? wrong event type? missing edge case?) and propose a fix to strengthen the existing hook or rule.

Also: if the user previously expressed a taste in this conversation that this hook missed as a false negative, write a hook for that too.
