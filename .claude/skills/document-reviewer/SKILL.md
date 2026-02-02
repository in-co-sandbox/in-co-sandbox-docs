---
name: document-reviewer
description: Review and improve Sandbox API documentation pages for quality, consistency, and AI-readability. Use when asked to review documentation, check docs quality, audit a page, improve documentation, or validate content against standards. Applies to MDX files in api-reference/, guides/, and recipes/ directories.
---

# Document Reviewer

Review Sandbox API documentation for quality, consistency, and modern documentation best practices.

## Review dimensions

Evaluate documentation across these ten dimensions (based on Lee Robinson's documentation principles):

| Dimension | Focus |
|:----------|:------|
| Readable | Concise, scannable, progressive complexity |
| Helpful | Workarounds documented, actionable guidance |
| AI-native | LLM-optimized, self-contained answers |
| Agent-ready | Easy to copy/paste as Markdown |
| Polished | Cross-linked, stable anchors, consistent |
| Accurate | Verified links, correct technical details |
| Structured | Proper components, frontmatter, hierarchy |
| Consistent | Matches existing patterns and style |
| Accessible | Alt text, semantic headings |
| Actionable | Clear next steps, working examples |

## Review workflow

### Step 1: Identify page type

Determine the page type from its path and structure:

| Path pattern | Page type | Key checks |
|:-------------|:----------|:-----------|
| `**/overview.mdx` | Product overview | Promise pattern, feature cards, FAQs |
| `**/endpoints/**` | API reference | Generated from OpenAPI, minimal review |
| `recipes/**` | Recipe/tutorial | Steps component, prerequisites, code examples |
| `guides/**` | Guide | Procedural content, prerequisites |

### Step 2: Run checklist for page type

#### All pages

- [ ] Frontmatter has `title` and `description`
- [ ] Description under 160 chars with keywords
- [ ] Sentence case for headings ("Getting started" not "Getting Started")
- [ ] No marketing language or superlatives
- [ ] Active voice, second person ("you")
- [ ] Internal links use relative paths
- [ ] Code blocks have language tags
- [ ] Images have alt text

#### Overview pages

See [OVERVIEW-CHECKLIST.md](references/OVERVIEW-CHECKLIST.md) for detailed requirements.

Quick checks:
- [ ] Two-part opening: definition sentence + promise sentence
- [ ] Feature cards in 2-column CardGroup
- [ ] Steps component for workflow
- [ ] API tables with links
- [ ] FAQ with self-contained answers (no "It is..." openers)

#### Recipe pages

- [ ] Prerequisites listed upfront
- [ ] Steps component with numbered workflow
- [ ] Code examples in Accordion (collapsible)
- [ ] Response field explanations
- [ ] Links to API reference docs

#### Guide pages

- [ ] Prerequisites at start
- [ ] Numbered steps for procedures
- [ ] Working code examples
- [ ] Cross-links to related content

### Step 3: Check AI-readability

Modern documentation is consumed by LLMs. Verify:

**FAQ answers are self-contained:**
```markdown
<!-- Bad -->
Q: What is DigiLocker?
A: It is a secure platform for documents.

<!-- Good -->
Q: What is DigiLocker?
A: DigiLocker is a government platform for storing and sharing documents digitally under the Digital India initiative.
```

**Content front-loads key information:**
- First sentence of each section contains the main point
- Important terms appear early, not buried in paragraphs

**Explicit over implicit:**
- Entity names repeated (not just "it" or "this API")
- Context included in each section (can be understood in isolation)

### Step 4: Validate technical accuracy

- [ ] All internal links resolve (`/api-reference/...`, `/guides/...`, `/recipes/...`)
- [ ] External links are functional
- [ ] API endpoints match OpenAPI spec
- [ ] Code examples are syntactically correct
- [ ] Headers and parameters are accurate

### Step 5: Generate review report

Structure feedback as:

```markdown
## Review: [Page title]

### Summary
[1-2 sentence overall assessment]

### Issues found

#### Critical (must fix)
- [Issue with specific location and fix]

#### Recommended (should fix)
- [Issue with specific location and fix]

#### Minor (nice to have)
- [Issue with specific location and fix]

### What's working well
- [Positive observations]
```

## Writing standards

### Language rules

| Rule | Bad | Good |
|:-----|:----|:-----|
| No promotional language | "powerful", "seamless", "revolutionary" | Describe what it does factually |
| Specific sources | "industry reports suggest" | Link to specific documentation |
| Avoid editorializing | "it's important to note" | State the information directly |
| No vague pronouns at start | "It provides..." | "[Product name] provides..." |
| Active voice | "can be used to" | "use this to" |

### Mintlify components

Verify correct component usage:

```mdx
<!-- Cards in 2-column grid -->
<CardGroup cols={2}>
  <Card title="Feature" icon="icon-name">
    Description with period.
  </Card>
</CardGroup>

<!-- Sequential workflow -->
<Steps>
  <Step title="Action verb + object">
    One sentence explanation.
  </Step>
</Steps>

<!-- FAQs -->
<AccordionGroup>
  <Accordion title="Question in natural language?">
    Self-contained answer starting with entity name.
  </Accordion>
</AccordionGroup>
```

### Link requirements

Minimum internal link counts:

| Section | Minimum links |
|:--------|:-------------:|
| API tables | 1 per row |
| Recipes section | 2+ |
| FAQs | 1-2 per answer (when relevant) |

## Common issues

Quick reference for frequent problems:

| Issue | Example | Fix |
|:------|:--------|:----|
| Title case headings | "How It Works" | "How it works" |
| Missing description period | `description: "Get started"` | `description: "Get started."` |
| Generic FAQ answers | "It is a platform..." | "DigiLocker is a platform..." |
| Marketing language | "powerful API" | "API for [specific function]" |
| Broken internal link | `(/api/endpoint)` | `(/api-reference/endpoint)` |
| Missing code language | ` ```\ncode\n``` ` | ` ```json\ncode\n``` ` |

## Output format

When reviewing, provide:

1. **Severity-ranked issues** - Critical → Recommended → Minor
2. **Specific locations** - Line numbers or section names
3. **Concrete fixes** - Show the corrected text
4. **Positive feedback** - What the page does well

Keep feedback actionable and specific. Avoid vague suggestions like "improve clarity"—instead show the exact change needed.
