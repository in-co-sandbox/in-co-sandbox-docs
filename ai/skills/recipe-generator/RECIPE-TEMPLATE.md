# Recipe template

Use this template structure when generating recipes.

## Complete template

```mdx
---
title: "{Action} {Entity}"
description: "{Concise description of what this recipe accomplishes and its business value. Include searchable terms.}"
---

{Optional: Brief intro paragraph if needed for context. Keep to 1-2 sentences max.}

<Info>
Before you begin:
- {Prerequisite 1 - e.g., authentication token requirement}
- {Prerequisite 2 - e.g., required data or prior steps}
- {Link to prerequisite recipe if applicable}
</Info>

<Steps>

  <Step title="{Action-oriented step title}" stepNumber={1} titleSize="h2">
    {Brief explanation of what this step does and why.}
    
    {If referencing an API, link to it}: Use the [**{API Name}**]({relative-path-to-api-reference}) endpoint.

    {Explain required inputs if not obvious from the code example.}

    <Accordion title="cURL Request" defaultOpen>
      ```bash
      curl --request {METHOD} \
        --url {endpoint-url} \
        --header 'authorization: {token-placeholder}' \
        --header 'x-api-key: xxxxxxxxxxxxx' \
        --header 'x-api-version: 1.0.0' \
        --header 'Content-Type: application/json' \
        --data '{
          "field": "value"
        }'
      ```
    </Accordion>

    {Explain response fields if user needs to save/use them in later steps.}

    {Optional callouts}:
    <Warning>
      {Critical warning about destructive action or common mistake}
    </Warning>

    <Tip>
      {Best practice or optimization suggestion}
    </Tip>
  </Step>

  <Step title="{Next step title}" stepNumber={2} titleSize="h2">
    {Continue pattern for each API call in the sequence}
  </Step>

</Steps>
```

## Element guidelines

### Step titles

- Start with verb: "Authenticate", "Generate", "Upload", "Fetch", "Verify"
- Be specific: "Generate OTP for CSI Download" not just "Generate OTP"
- Keep concise: 5-8 words maximum

### API links

Use relative paths from the recipe location:

```markdown
[**Generate E-Invoice**](../../../api-reference/gst/compliance/endpoints/e-invoice/generate_e_invoice)
```

Path pattern: `../../../api-reference/{workload}/{subgroup}/endpoints/{category}/{endpoint}`

### Token placeholders

Use consistent placeholder names:
- `{sandbox-access-token}` - Main Sandbox JWT token
- `{e-invoice-access-token}` - E-Invoice specific token
- `{taxpayer-access-token}` - Taxpayer session token

### Response explanations

After code examples, list important response fields:

```markdown
When successful, you'll receive:
- **field_name** - Description of what this is and how to use it
- **another_field** - Description

Save these values for use in the next step.
```

Or use ParamField for structured responses:

```markdown
<ParamField body="session_id" type="string" required>
  A unique identifier used to track this session.
</ParamField>
```

### Callout usage

| Callout | Use for |
|---------|---------|
| `<Info>` | Prerequisites, requirements before starting |
| `<Warning>` | Destructive actions, common mistakes, critical requirements |
| `<Tip>` | Optimizations, best practices, pro tips |
| `<Note>` | Helpful context, supplementary information |

### Polling patterns

For async/job-based APIs:

```markdown
<Step title="Check job status" stepNumber={N} titleSize="h2">
  Poll the job status endpoint until `status` is `succeeded`.

  <Accordion title="cURL Request" defaultOpen>
    ```bash
    curl --request GET \
      --url 'https://api.sandbox.co.in/{path}?job_id={job_id}' \
      ...
    ```
  </Accordion>

  When `status` is `succeeded`, the response includes:
  - **download_url** - Signed URL to download the result (time-limited)
</Step>
```

### File upload patterns

```markdown
<Step title="Upload file" stepNumber={N} titleSize="h2">
  Upload the file using the signed URL from the previous step.

  <Accordion title="cURL – Upload file">
    ```bash
    curl --request PUT \
      --url '{signed_upload_url}' \
      --header 'Content-Type: {mime-type}' \
      --data-binary '@/path/to/file.ext'
    ```
  </Accordion>
</Step>
```

## Category card format

When adding to introduction.mdx:

```mdx
<Card title="{Recipe Title}" icon="hat-chef" href="./{category}/{recipe_filename}">
</Card>
```
