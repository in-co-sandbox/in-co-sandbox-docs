---
description: Create a new documentation page with proper structure and Mintlify components. Guides you through page type selection and content creation. Use when asked to create a new page, add documentation, or write new content.
argument-hint: [page-type] [topic]
---

I need to create a new documentation page. Please help me:

1. **Determine the page type** based on $ARGUMENTS or ask me:
   - **Guide/Tutorial**: Step-by-step instructions to accomplish a goal
   - **API Reference**: Document an API endpoint with parameters and responses
   - **Concept/Overview**: Explain a feature or concept
   - **Recipe**: Quick solution to a specific problem
   - **Troubleshooting**: Help users solve common issues

2. **Create the frontmatter**:
   ```yaml
   ---
   title: "Clear, descriptive title"
   description: "What users will learn or accomplish"
   ---
   ```

3. **Structure the content** with appropriate components:
   - Use `<Steps>` for procedures
   - Use `<CodeGroup>` for multi-language examples
   - Use callouts (`<Note>`, `<Warning>`, `<Tip>`) appropriately
   - Use `<Card>` components for navigation to related content

4. **Include essential elements**:
   - Prerequisites at the start
   - Clear code examples with language tags
   - Expected outcomes and verification steps
   - Troubleshooting tips for complex procedures
   - Next steps or related content links

5. **Suggest the file location** and navigation placement in docs.json

$ARGUMENTS
