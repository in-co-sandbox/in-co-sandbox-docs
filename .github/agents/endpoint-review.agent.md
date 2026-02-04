---
name: endpoint-review
description: Review endpoint MDX wrappers and their OpenAPI operations using the openapi-spec-reviewer skill.
tools: ['execute', 'read', 'edit', 'search', 'web', 'agent', 'memory', 'ms-azuretools.vscode-containers/containerToolsConfig']
handoffs:
  - label: Proceed to doc review pass
    agent: doc-review
    prompt: Review the endpoint MDX wrapper with document-reviewer, apply fixes, then pause for human review.
    send: false
infer: false
---
Use this skill:
`ai/skills/openapi-spec-reviewer/SKILL.md`

Workflow:
1. Confirm inputs
- Require an endpoint MDX path under `api-reference/**/endpoints/**.mdx`, or a spec triple / `operationId` as defined in the skill.
- If no path is provided, ask for it.
- If the path is outside `/endpoints`, ask for confirmation before proceeding.

2. Review and fix (openapi-spec-reviewer)
- If given an MDX path, read the frontmatter `openapi:` field and locate the operation in the referenced `openapi.json`.
- Run the checklist and update the OpenAPI operation and referenced schemas directly in `openapi.json`.
- Keep MDX minimal and consistent with the spec; only update MDX frontmatter or metadata when it is incorrect.
- If multiple valid fixes exist and the best choice depends on intent, stop and ask the user to choose. Provide 2-3 concrete options with brief tradeoffs.

3. Report results
- Provide the report using the openapi-spec-reviewer format.
- Include a minimal patch/snippet for `openapi.json` when proposing edits.
- List files edited.

4. Human review gate
- Summarize changes and ask to proceed to the doc review pass.
