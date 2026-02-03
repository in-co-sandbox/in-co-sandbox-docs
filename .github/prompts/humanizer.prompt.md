---
name: humanizer
description: Remove “AI-written” patterns from the current MDX prose while keeping facts unchanged.
agent: edit
---

Follow this skill guide:
[Skill: humanizer](../../.github/skills/humanizer/SKILL.md)

Target:
- If I have a selection, humanize only that.
- Otherwise, humanize the current section in the active editor.

Constraints (must follow):
- Preserve meaning, numbers, API names, parameter names, and compliance terms.
- Remove generic/salesy tone, repetition, filler phrases, and over-formality.
- Avoid em-dash overuse and “rule of three” rhythm.

Output:
- Apply edits directly to the text.
