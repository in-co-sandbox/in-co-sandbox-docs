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
- `.agents/`: AI agents and skills
  - `.agents/agents/`: Agent definitions for documentation workflow
  - `.agents/skills/`: Reusable skills for documentation quality, SEO/GEO, and content review
- `.github/instructions/`: path-specific writing rules

## Agents and skills

This repo uses a multi-agent documentation review pipeline:

### Agent workflow
1. **doc-quality-bot**: Entry point that routes to appropriate review agent
2. **endpoint-review**: Reviews API endpoint MDX + OpenAPI specs
3. **doc-review**: Reviews content quality and applies SEO/GEO optimization (mandatory)
4. **clarity**: Improves writing clarity and concision
5. **humanizer**: Removes AI-sounding patterns

### Available skills
All skills are located in `.agents/skills/`:
- **document-reviewer**: Quality checks for API docs
- **seo-geo**: SEO & GEO optimization for search engines and AI (ChatGPT, Perplexity, etc.)
- **openapi-spec-reviewer**: OpenAPI spec validation
- **writing-clearly-and-concisely**: Clarity and concision improvements
- **humanizer**: Remove AI writing patterns
- **recipe-generator**: Generate workflow recipes
- **update-nav**: Update docs.json navigation
- **mintlify**: Mintlify component usage
- **skill-creator**: Create new skills

### SEO/GEO optimization
The doc-review agent mandatorily applies SEO/GEO improvements to all pages:
- Optimized frontmatter keywords and descriptions
- Statistics and data points (+37% AI visibility)
- Authoritative citations (+40% AI visibility)
- FAQ sections with LLM-optimized answers (+40% AI citation rate)
- Technical terminology and domain authority

## Writing conventions
- Use MDX with YAML frontmatter. For new pages include `title`, `description`, and `keywords`.
- Use sentence case headings and second-person voice.
- Prefer active voice, short sentences, and concrete language.
- Avoid promotional language and emojis.
- Use root-relative links for internal docs.
- Add language tags to all code blocks.
- Provide descriptive alt text for images.

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
