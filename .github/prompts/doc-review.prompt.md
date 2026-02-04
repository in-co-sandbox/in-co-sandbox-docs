---
agent: 'doc-quality-bot'
description: 'Review a documentation file with the doc-quality-bot entrypoint (routes endpoint docs to openapi review first).'
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'agent', 'memory', 'todo']
---

## Task

Review documentation using the `doc-quality-bot` pipeline.

## Required input

- **File path**: An `.mdx` file under `api-reference/`, `guides/`, or `recipes/`.

If the file is under `api-reference/**/endpoints/**.mdx`, the entrypoint will route to `endpoint-review` first and then `doc-review`. Otherwise it will go directly to `doc-review`.

## What to do

1. If the file path is missing, ask for it.
2. Confirm the file is eligible.
3. Start the review pipeline.
