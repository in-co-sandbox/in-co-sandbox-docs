# AGENTS.md

## Project overview
- This repo contains Sandbox API documentation built with Mintlify (MDX).
- Most content lives in `api-reference/`, `guides/`, and `recipes/`.
- Navigation and site config live in `docs.json`.

## Setup commands
- Install Mintlify CLI: `npm i -g mint`
- Preview docs locally: `mint dev` or `npx mint dev` (run from the repo root)
- Troubleshooting CLI: `mint update`

## Repo layout
- `api-reference/`: API reference pages (MDX)
- `guides/`: product and developer guides (MDX)
- `recipes/`: workflow recipes (MDX)
- `static/`: images and static assets
- `data/`: shared data files
- `.github/instructions/`: path-specific writing rules

## Writing conventions
- Use MDX with YAML frontmatter. For new pages include `title`, `description`, and `keywords`.
- Use sentence case headings and second-person voice.
- Prefer active voice, short sentences, and concrete language.
- Avoid promotional language and emojis.
- Use root-relative links for internal docs.
- Add language tags to all code blocks.
- Provide descriptive alt text for images.
- Use kebab-case for new file names.

## Path-specific instructions
- If editing `**/overview.mdx` or `**/introduction.mdx`, follow `.github/instructions/product-overview.instructions.md`.
- Check `.github/instructions/**/*.instructions.md` for other file-specific rules.

## Navigation
- When you add a new page, update `docs.json` to include it in the correct section.

## Quality checks
- Verify internal links work.
- Preview with `mint dev` when changes affect layout or components.
- Check for broken links: `npx mint broken-links`

## Windows and symlinks
- This repo uses symlinks. On Windows, enable Developer Mode so the Mintlify server can start.

## Boundaries
- Always: keep changes scoped to the requested docs and match existing patterns.
- Ask first: large rewrites, renaming or moving files, adding new pages not requested by the user, or structural changes to `docs.json`.
- Never: add secrets or credentials, or modify generated build output.
