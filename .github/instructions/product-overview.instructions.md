---
applyTo: "**/overview.mdx"
---

# Product Overview Page Instructions

These instructions apply when creating or editing product overview pages (overview.mdx or introduction.mdx files) in the Sandbox documentation. The goal is to communicate product value clearly while boosting SEO discoverability.

## Required Prompt Inputs (MANDATORY)

**DO NOT create an overview page unless the user provides ALL of the following inputs.** If any are missing, ask the user to provide them before proceeding.

| Input | Description | Example |
|:------|:------------|:--------|
| **Product name** | Official API/product name for H1 | "DigiLocker API", "GSTR-1 API" |
| **Definition** | One sentence: what the product IS | "Government platform for document storage" |
| **Promise** | One sentence: what user CAN DO | "Retrieve Aadhaar, PAN, driving license" |
| **Compliance context** | Regulatory/legal framework | "UIDAI guidelines", "GST portal", "RBI KYC" |
| **Workflow steps** | 3-8 sequential steps | "1. Initiate session → 2. Authenticate → 3. Fetch" |
| **API endpoints** | List with paths | "Generate OTP: /api/auth/otp" |
| **Use cases** | 3-6 real-world scenarios | "Verify identity during onboarding" |

### Validation Checklist

Before generating content, confirm:

- [ ] Product name is provided (not generic like "the API")
- [ ] Definition sentence includes primary keyword
- [ ] Promise sentence starts with action verb
- [ ] At least 2 workflow steps are listed
- [ ] At least 2 API endpoints with paths are provided
- [ ] At least 2 use cases are specified

### If Inputs Are Missing

Respond with:

```
To create a complete overview page, I need the following information:

1. **Product name**: What is the official name of this API?
2. **Definition**: In one sentence, what is this product?
3. **Promise**: What can users do with this API?
4. **Compliance context**: What regulations or standards does this relate to?
5. **Workflow steps**: What are the main steps to use this API? (3-8 steps)
6. **API endpoints**: List the key endpoints with their paths
7. **Use cases**: What are 3-6 real-world scenarios for this API?

Please provide these details and I'll generate the overview page.
```

### Optional Inputs (Copilot Can Infer)

These can be derived if not provided:
- FAQ questions (generate from product context)
- Icons (use icon mapping in this document)
- Recipes (search `/recipes/` directory)
- SDK alternatives (search for `-sdk` directories)

## Page Structure

Follow this structure for all product overview pages:

1. **Frontmatter** - Title and description (SEO-critical)
2. **H1 heading** - Product name with "API" suffix
3. **Promise line + explanation** - Two-part opening (see below)
4. **Value proposition** - Brief statement on compliance/business value
5. **Feature cards** - 2-column CardGroup highlighting key capabilities
6. **How it works** - Steps component showing the workflow
7. **What you can do / Recipes** - CardGroup linking to detailed guides
8. **API categories** - CardGroup organizing endpoints by function
9. **API tables** - Reference tables with links to endpoints
10. **Common use cases** - Bullet list of real-world applications
11. **FAQ section** - AccordionGroup answering common questions

## Frontmatter Guidelines

```yaml
---
title: "Overview"  # Keep simple and consistent
description: "Action-oriented description with primary keywords, max 160 chars"
---
```

- Include primary product keywords in description
- Use action verbs: "Retrieve", "File", "Verify", "Calculate"
- Mention key compliance or regulatory context (GST, KYC, RBI, UIDAI)
- Keep description under 160 characters for SEO

## Writing Style

- **Be concise**: One sentence per concept
- **Lead with value**: What problem does this solve?
- **Use active voice**: "Use this API to..." not "This API can be used to..."
- **Include compliance context**: Mention relevant regulations (UIDAI, RBI, GST)
- **Avoid jargon**: Explain technical terms when first used

## Promise Line Pattern

The opening must follow a two-part structure:

1. **Definition sentence** (what it is): Establish the product identity with keywords
2. **Promise sentence** (what you can do): Action-oriented value proposition

### Examples

**DigiLocker API:**
> DigiLocker is a government platform for storing and sharing documents digitally. Use this API to retrieve government-issued documents from your users' DigiLocker accounts after they grant consent.

**GSTR-1 API:**
> GSTR-1 is a monthly or quarterly return for reporting outward supplies (sales). Use these APIs to save invoice data, retrieve summaries, and file returns directly to the GST portal.

### Pattern Template
```
[Product] is [definition with primary keyword]. Use this API to [primary action verb] + [what user achieves] + [context/compliance benefit].
```

## Required Mintlify Components

### CardGroup for features (always 2 columns)
```mdx
<CardGroup cols={2}>
  <Card title="Feature name" icon="icon-name">
    Brief description of the capability and its benefit.
  </Card>
</CardGroup>
```

### Steps for workflow
```mdx
<Steps>
  <Step title="Action verb + object">
    One sentence explaining this step.
  </Step>
</Steps>
```

### AccordionGroup for FAQs
```mdx
<AccordionGroup>
  <Accordion title="Question in natural language?">
    Answer in 1-3 sentences. Use formatting for clarity.
  </Accordion>
</AccordionGroup>
```

## Icon Selection

Use Font Awesome icons that match the concept:
- Authentication: `shield-check`, `key`, `lock`
- Documents: `file-lines`, `file-invoice`, `folder`
- Verification: `circle-check`, `badge-check`
- Data/API: `database`, `code`, `server`
- Filing/Submit: `paper-plane`, `file-circle-check`
- Users: `users`, `user`, `id-card`
- Mobile: `mobile`, `mobile-screen`
- Errors: `triangle-exclamation`

## API Reference Tables

Use consistent table format with three columns:

```markdown
| API | Purpose |
|:----|:--------|
| [API Name](/path/to/endpoint) | Brief description |
```

Or with additional context:

```markdown
| API | Table/Code | Description |
|:----|:-----------|:------------|
| [API Name](/path/to/endpoint) | Reference | Detailed description |
```

## SEO Best Practices

1. **H1 should contain product name**: "DigiLocker API", "GSTR-1 API"
2. **Use semantic headings**: H2 for sections, H3 for subsections
3. **Include keyword variations**: "DigiLocker", "Digi Locker", "digital locker"
4. **Link internally**: Cross-reference related APIs and guides
5. **Answer search queries in FAQs**: Use natural question phrasing

## Common Use Cases Section

Format as a brief intro followed by bullet points:

```markdown
## Common use cases

Use [Product] API when you need to:

- First use case with specific context
- Second use case with business benefit
- Third use case mentioning integration scenario
```

## FAQ Guidelines

Include 5-8 questions covering:
1. What is [Product]? - Basic definition
2. How does it work? - High-level flow
3. What data/documents can I access? - Capabilities
4. What are the prerequisites? - Requirements
5. Integration questions - SDK vs API differences
6. Session/authentication questions - Technical details
7. Compliance/regulatory questions - Legal context

### LLM Retrieval Optimization

FAQs are consumed by LLMs for RAG (Retrieval Augmented Generation). Follow these rules:

- **Self-contained answers**: Each answer must make sense without reading the question or page context
- **Repeat entity names**: Include product name in answers, not just questions
- **Front-load key facts**: Put the most important information in the first sentence
- **Avoid pronouns at start**: Don't begin with "It", "This", "They"—use the actual noun

**Bad:**
```
Q: What is DigiLocker?
A: It is a secure cloud-based platform for documents.
```

**Good:**
```
Q: What is DigiLocker?
A: DigiLocker is a flagship initiative under Digital India Mission—a secure cloud-based platform for storage, sharing and verification of documents & certificates.
```

## Cross-linking

Always link to:
- Related recipes in `/recipes/` directory
- Authentication endpoints
- Error handling guide at `/guides/developer-resources/errors`
- SDK alternatives when available

### Internal Link Density Requirements

Maintain minimum link counts per section for crawlability and navigation:

| Section | Minimum Links |
|:--------|:-------------:|
| Feature cards (CardGroup) | 0 (icons only) |
| How it works (Steps) | 0 (workflow focus) |
| API categories (CardGroup) | 4+ |
| API tables | 1 per row |
| Recipes section | 2+ |
| FAQs | 1-2 per answer when relevant |

### Link Text Best Practices

- Use descriptive anchor text, not "click here" or "learn more"
- Include the API or feature name in link text
- Prefer relative paths: `/api-reference/...` over full URLs
- Link to the most specific page (endpoint > overview > product)

## Do Not

- Use marketing language or superlatives ("best", "revolutionary")
- Include pricing information
- Add version-specific details that may become outdated
- Repeat the same information in multiple sections
- Use abbreviations without first defining them
