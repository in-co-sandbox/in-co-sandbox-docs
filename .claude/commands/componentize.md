---
description: Convert plain content into proper Mintlify component structure. Transforms markdown into Steps, CodeGroups, Callouts, and other components. Use when asked to componentize, restructure, or convert documentation.
argument-hint: [file-path]
---

Transform the content in $ARGUMENTS to use appropriate Mintlify components:

## Transformation rules

### Sequential instructions → Steps
```mdx
<Steps>
<Step title="First step">
  Instructions with optional code or callouts.
</Step>
<Step title="Second step">
  More instructions.
</Step>
</Steps>
```

### Important notices → Callouts
- Warnings about destructive actions → `<Warning>`
- Best practices and tips → `<Tip>`
- Prerequisites and requirements → `<Info>`
- Helpful extra context → `<Note>`
- Success confirmations → `<Check>`

### Multi-language code → CodeGroup
```mdx
<CodeGroup>
```javascript Node.js
// code
```
```python Python
# code
```
</CodeGroup>
```

### Platform alternatives → Tabs
```mdx
<Tabs>
<Tab title="Production">
  Production-specific content
</Tab>
<Tab title="Staging">
  Staging-specific content
</Tab>
</Tabs>
```

### Optional/supplementary content → Accordion
```mdx
<AccordionGroup>
<Accordion title="Advanced configuration">
  Optional details here
</Accordion>
</AccordionGroup>
```

### Related links → Cards
```mdx
<CardGroup cols={2}>
<Card title="Related topic" icon="icon-name" href="/path">
  Brief description
</Card>
</CardGroup>
```

### Images → Frame
```mdx
<Frame caption="Optional caption">
<img src="/path/to/image.png" alt="Descriptive alt text" />
</Frame>
```

Please analyze the file and apply appropriate transformations while preserving the content meaning.

$ARGUMENTS
