---
name: document-reviewer
description: Audit this MDX doc for quality + AI-readability, then apply improvements.
agent: edit
---

Use this review standard:
[Skill: document-reviewer](../../.github/skills/document-reviewer/SKILL.md)

Task:
1) Identify issues (missing prerequisites, unclear steps, inconsistent terms, marketing fluff, weak headings, poor scannability).
2) Fix them while preserving meaning and product constraints.
3) Improve LLM-readability (explicit steps, clear definitions, consistent naming, fewer ambiguous pronouns).

Constraints:
- Preserve facts and flows.
- Don’t invent endpoints or capabilities.
- Keep code blocks and API examples correct; only edit them if clearly wrong.

Output:
- Apply edits directly in the current MDX file.
