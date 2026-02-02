# Overview Page Checklist

Detailed review checklist for product overview pages (`**/overview.mdx`).

## Structure requirements

### 1. Frontmatter

```yaml
---
title: "Overview"
description: "Action verb + primary keywords + compliance context, max 160 chars"
---
```

- [ ] Title is "Overview" (simple and consistent)
- [ ] Description starts with action verb (Retrieve, File, Verify, Generate)
- [ ] Description includes primary product keywords
- [ ] Description mentions compliance/regulatory context (GST, KYC, RBI, UIDAI)
- [ ] Description under 160 characters

### 2. Opening section

Must follow the two-part promise pattern:

```markdown
# [Product Name] API

[Definition sentence - what it IS]. [Promise sentence - what you CAN DO].
```

**Examples:**

```markdown
# DigiLocker API

DigiLocker is a government platform for storing and sharing documents digitally. 
Use this API to retrieve government-issued documents from your users' DigiLocker 
accounts after they grant consent.
```

```markdown
# GST e-Invoice API

GST e-Invoice is a GST-compliant invoice with a unique IRN (Invoice Reference Number). 
Use this API to generate IRNs, receive signed invoice + signed QR code, download a 
PDF copy, cancel or fetch e-invoices, and generate/fetch E-Way Bills linked to the IRN.
```

**Checklist:**
- [ ] H1 contains product name with "API" suffix
- [ ] First sentence defines what the product IS (include primary keyword)
- [ ] Second sentence states what user CAN DO (start with action verb)
- [ ] Both sentences are concise (one sentence each)

### 3. Feature cards

```mdx
<CardGroup cols={2}>
  <Card title="Feature name" icon="icon-name">
    Brief description of the capability and its benefit.
  </Card>
</CardGroup>
```

- [ ] Uses `CardGroup` with `cols={2}`
- [ ] 4-6 cards highlighting key capabilities
- [ ] Each card has descriptive title
- [ ] Each card has appropriate Font Awesome icon
- [ ] Card descriptions end with periods
- [ ] No marketing language in descriptions

### 4. How it works

```mdx
<Steps>
  <Step title="Action verb + object">
    One sentence explaining this step.
  </Step>
</Steps>
```

- [ ] Uses `Steps` component
- [ ] Step titles start with action verbs (Create, Authenticate, Generate)
- [ ] 3-8 steps covering the complete workflow
- [ ] Each step has one-sentence explanation
- [ ] Steps link to relevant API endpoints or guides

### 5. API tables

```markdown
| API | Purpose |
|:----|:--------|
| [API Name](/path/to/endpoint) | Brief description |
```

- [ ] Organized by logical categories (Authentication, Operations, etc.)
- [ ] Every row has a working internal link
- [ ] Purpose column is concise (under 80 chars)
- [ ] Uses consistent table format throughout

### 6. Common use cases

```markdown
## Common use cases

Use [Product] API when you need to:

- First use case with specific context
- Second use case with business benefit
- Third use case mentioning integration scenario
```

- [ ] Brief intro followed by bullet list
- [ ] 4-6 concrete use cases
- [ ] Each bullet is specific (not generic)
- [ ] Mentions real-world scenarios

### 7. FAQ section

```mdx
<AccordionGroup>
  <Accordion title="Question in natural language?">
    [Entity name] + answer content. Self-contained.
  </Accordion>
</AccordionGroup>
```

**Critical AI-readability rules:**

- [ ] 5-8 questions covering common queries
- [ ] Answers are SELF-CONTAINED (make sense without reading question)
- [ ] Answers START WITH ENTITY NAME (not "It", "This", "They")
- [ ] First sentence contains the key fact
- [ ] Relevant answers include internal links

**Question coverage:**
- [ ] What is [Product]?
- [ ] How does it work?
- [ ] What data/documents can I access?
- [ ] What are the prerequisites?
- [ ] Common integration questions
- [ ] Compliance/regulatory questions

## Content quality

### Writing style

- [ ] Active voice throughout
- [ ] Second person ("you")
- [ ] Sentence case for all headings
- [ ] No marketing language ("powerful", "seamless", "revolutionary")
- [ ] No editorializing ("it's important to note", "as mentioned above")
- [ ] Concise sentences (one idea per sentence)

### Internal linking

Minimum link counts:
- [ ] API tables: 1 link per row
- [ ] How it works: Links to key endpoints
- [ ] FAQs: 1-2 links per answer (when relevant)
- [ ] Related recipes referenced

### Technical accuracy

- [ ] All internal links resolve
- [ ] API endpoint paths match OpenAPI spec
- [ ] Compliance references are current (UIDAI, GST, RBI guidelines)

## Common problems

| Problem | Location | Fix |
|:--------|:---------|:----|
| Missing promise pattern | Opening section | Add definition + promise sentences |
| Title case headings | Throughout | Convert to sentence case |
| Generic FAQ answers | FAQ section | Start with entity name, add context |
| Missing card icons | Feature cards | Add appropriate Font Awesome icon |
| 1-column CardGroup | Feature cards | Change to `cols={2}` |
| Steps without links | How it works | Add links to endpoints/guides |
| Vague use cases | Common use cases | Add specific context and scenarios |
