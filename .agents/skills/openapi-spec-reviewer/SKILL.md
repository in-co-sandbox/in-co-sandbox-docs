---
name: openapi-spec-reviewer
description: "Review and improve OpenAPI (OAS 3.0/3.1) specs so they read like high-quality documentation. Use when asked to audit or edit an openapi.json file, improve operation summaries/descriptions/examples, validate doc quality for a specific endpoint referenced by an api-reference/**/endpoints/**.mdx file (via its frontmatter openapi: 'SPEC METHOD PATH' field), or produce a severity-ranked report with concrete OpenAPI changes."
---

# OpenAPI Spec Reviewer

## Overview

Use this skill to review an OpenAPI operation (and its schemas) for documentation quality, using this docs repo's endpoint MDX wrappers as the entry point.

## Inputs

Provide one of:

- An endpoint MDX wrapper file path (preferred): `api-reference/**/endpoints/**.mdx`
- A spec triple: `api-reference/**/openapi.json` + HTTP method + route path
- An `operationId` (use it as a lookup key inside the spec)

## Workflow

### Step 1: Locate the operation in `openapi.json`

If given an endpoint MDX file:

- Read the frontmatter `openapi:` field. It is formatted as: `<specPath> <METHOD> <PATH>`.
- Map `specPath` from docs URL-style to repo path by removing the leading `/`.
- Open the spec file (usually `api-reference/**/openapi.json`).
- Find the operation at `paths[PATH][methodLower]`.

Optional helper (recommended for speed and fewer mistakes):

```powershell
python -X utf8 .agents/skills/openapi-spec-reviewer/scripts/review_openapi_operation.py `
  --mdx api-reference/gst/compliance/endpoints/e-way-bill/authenticate.mdx
```

If given a spec triple (spec file + method + path):

```powershell
python -X utf8 .agents/skills/openapi-spec-reviewer/scripts/review_openapi_operation.py `
  --spec api-reference/gst/compliance/openapi.json `
  --method POST `
  --path /gst/compliance/e-way-bill/tax-payer/authenticate
```

### Step 2: Run the doc-quality checklist (operation level)

Treat these as guidelines; apply judgement based on the endpoint.

#### Critical (must fix)

- `summary` exists and is specific (not "OK" / "Success")
- `operationId` exists, is unique, and is stable across releases
- `responses` exists and includes at least one success response (`200`, `201`, `202`, `204`, `2XX`)
- Every response has a non-empty `description`
- Response bodies have a `schema` (or intentionally have no body for status like `204`)

#### Recommended (should fix)

- `description` explains what the endpoint does, when to use it, and any prerequisites
- Parameters have `description`, `required`, and constraints (`format`, `pattern`, `minLength`, `maxLength`, etc.)
- Request body includes at least one concrete example
- Request body has a schema. For complex bodies (>5 fields), prefer a component schema via `$ref` instead of a large inline schema.
- Success response includes at least one concrete example
- Common error responses are documented (at least `400` + auth-related errors if applicable), using a consistent error schema
- `tags` are present and consistent (avoid tag sprawl/typos)

#### Minor (nice to have)

- `externalDocs` links to a longer guide (when one exists)
- Operation notes cover idempotency, retries, rate limits, and side effects (when relevant)
- Examples cover at least one common failure case

### Step 3: Review schemas referenced by the operation

- Follow `$ref` chains from request/response schemas into `components/schemas`.
- Ensure the schema has a clear `description`.
- Ensure every property has a `description` (especially IDs, dates, enums, and money fields).
- Add field-level constraints and examples where it prevents misuse.
- Prefer reuse via `$ref` for repeated schemas (errors, pagination objects, common headers).

### Step 4: Cross-check the endpoint MDX wrapper (if present)

- Verify the MDX `title`/`description` are consistent with the operation intent.
- Verify the frontmatter `openapi:` reference matches the spec (method + path).
- Avoid duplicating long-form details in MDX that will drift from the spec; prefer making the spec the source of truth.

### Step 5: Produce a review report with concrete changes

Output a Markdown report with:

- Operation identity: spec file path + method + path + `operationId`
- 1–2 sentence summary
- Issues grouped by **Critical**, **Recommended**, **Minor**
- For each issue: include a JSON Pointer (example: `#/paths/~1gst~1compliance~1.../post/summary`) and a suggested fix
- If proposing edits: show a minimal patch/snippet for `openapi.json`

## References

- Use `references/openapi-doc-best-practices-resources.md` for deeper guidance and links (OAS, Learn OpenAPI, Spectral, Redocly, and general API design guidelines).
