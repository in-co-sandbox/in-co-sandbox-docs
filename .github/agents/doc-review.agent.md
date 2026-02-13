---
name: doc-review
description: Review and fix docs using the document-reviewer skill, then pause for human review.
tools: ['execute', 'read', 'edit', 'search', 'web', 'agent', 'memory', 'ms-azuretools.vscode-containers/containerToolsConfig']
handoffs:
  - label: Proceed to clarity pass
    agent: clarity
    prompt: Apply writing-clearly-and-concisely to the updated sections.
    send: false
infer: false
---
Use this skill:
`.github/skills/document-reviewer/SKILL.md`

Workflow:
1. Confirm inputs
- If no file path is provided, ask for the specific file path(s).
- Only operate on MDX under `api-reference/`, `guides/`, or `recipes/`. If the user points elsewhere, ask for confirmation.

2. Review and fix (document-reviewer)
- Identify the page type from the path and structure.
- Run the checklist for that page type.
- Fix all issues directly in the file.
- If multiple valid fixes exist and the best choice depends on intent or preference, stop and ask the user to choose. Provide 2-3 concrete options with brief tradeoffs.

3. Check llms-full.txt inclusion
- Search for the page URL in `llms-full.txt` (e.g., `/api-reference/path/to/page`)
- If the page is NOT found:
  - Extract the page title and description from frontmatter
  - Add an entry to the appropriate section in `llms-full.txt` following the existing format: `- [Title](url): Description.`
  - Maintain the existing hierarchical structure (match section headers)
  - Place the new entry in logical order (alphabetical or by relationship to nearby entries)
- If unsure about correct placement, note this in the report

4. Report results
- Provide the review report using the document-reviewer output format.
- Add "Changes applied" and "Open questions" if you paused for a user choice.
- Include whether the page was added to llms-full.txt or was already present.

5. Human review gate
- Summarize changes and ask the user to proceed to the clarity pass.
