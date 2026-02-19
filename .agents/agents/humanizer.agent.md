---
name: humanizer
description: Remove AI-sounding patterns without changing meaning.
tools: ['execute', 'read', 'edit', 'search', 'web', 'agent', 'memory', 'ms-azuretools.vscode-containers/containerToolsConfig']
infer: false
---
Use this skill:
`.agents/skills/humanizer/SKILL.md`

Workflow:
1. Apply humanizer pass
- Edit the latest version of the prose.
- Preserve meaning, numbers, API names, parameter names, and compliance terms.
- If multiple valid fixes exist and the best choice depends on intent or preference, stop and ask the user to choose. Provide 2-3 concrete options with brief tradeoffs.

2. Summarize changes
- Provide a concise summary of edits.
