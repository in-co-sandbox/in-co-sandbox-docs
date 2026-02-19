---
name: recipe-generator
description: Generate API recipe documentation from a sequence of API endpoints. Creates step-by-step workflow guides using Mintlify components. Use when asked to create a recipe, generate a recipe, or build a workflow guide from API endpoints.
---

# Recipe Generator

Generate production-ready recipe documentation for Sandbox API workflows.

## When to use

- User provides a list of API endpoints to call in sequence
- User wants to create a step-by-step workflow guide
- User provides links to Sandbox API reference documentation

## Required inputs

The user must provide:

1. **Recipe title and description** - What the recipe accomplishes
2. **API steps** - Numbered list of API endpoints in sequence
3. **API reference links** - Links to hosted Mintlify docs (e.g., `https://docs.sandbox.co.in/api-reference/...`)
4. **Output path** - Where to save the recipe file (e.g., `recipes/gst/e-invoice/cancel_e_invoice.mdx`)
5. **Prerequisites** - Any prerequisite recipes or conditions (optional)

## Workflow

### Step 1: Gather information

If any required input is missing, ask the user:
- What is the recipe title and description?
- What are the API endpoints in sequence?
- What are the API reference documentation links?
- Where should this recipe be saved?
- Are there any prerequisite recipes to reference?

### Step 2: Fetch API documentation

Use the `fetch_webpage` tool to read each API reference page and extract:
- Endpoint URL and HTTP method
- Required headers
- Request body schema and example
- Response fields and their purposes
- Any important notes or warnings

### Step 3: Generate recipe content

Create the recipe file following the structure in [RECIPE-TEMPLATE.md](RECIPE-TEMPLATE.md).

Key elements:
- **Frontmatter**: SEO-optimized title and description
- **Steps component**: Each API call becomes a step
- **Accordion for code**: cURL examples in collapsible sections
- **Callouts**: Prerequisites in `<Info>`, warnings in `<Warning>`, tips in `<Tip>`
- **API links**: Link to API reference docs using relative paths
- **Response guidance**: Explain important response fields and what to do with them

### Step 4: Update navigation

After creating the recipe, update the workload's `introduction.mdx` to add a card linking to the new recipe.

Determine the workload from the output path:
- `recipes/gst/` → GST workload
- `recipes/kyc/` → KYC workload
- `recipes/tds/` → TDS workload
- `recipes/it/` → Income Tax workload

Add a new card under the appropriate category section.

### Step 5: Confirm with user

Show the user:
- Created recipe file path
- Updated introduction.mdx changes
- Any issues or missing information

## SEO best practices

### Frontmatter

```yaml
---
title: "Action-oriented title"  # Start with verb: Generate, File, Fetch, Create
description: "Concise 1-2 sentence description explaining what the recipe does and its business value. Include key terms users might search for."
---
```

**Title guidelines**:
- Start with action verb (Generate, File, Create, Fetch, Cancel)
- Include the main entity (E-Invoice, GSTR-1, Form 16)
- Keep under 60 characters

**Description guidelines**:
- Explain what the recipe accomplishes
- Include business context
- Mention key API actions
- Keep under 160 characters for SEO

### Content structure

- Use `<Steps>` for the sequential workflow
- Each step has a clear, action-oriented title
- Link to API reference for each endpoint
- Explain the purpose before showing code
- Describe what to do with response data

## File structure

```
recipes/
├── {workload}/              # gst, kyc, tds, it
│   ├── introduction.mdx     # Update with new card
│   └── {category}/          # e-invoice, authentication, form-24q, etc.
│       └── {recipe_name}.mdx
```

## Output format

See [RECIPE-TEMPLATE.md](RECIPE-TEMPLATE.md) for the complete template structure.
