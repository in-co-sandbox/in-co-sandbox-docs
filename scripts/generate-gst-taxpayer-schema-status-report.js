const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const MDX_ROOT = path.join(ROOT, 'api-reference', 'gst', 'compliance', 'endpoints', 'taxpayer');
const OUTPUT_FILE = path.join(MDX_ROOT, 'schema-status-report.md');
const GENERATED_ON = '2026-04-13';

function walk(dir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walk(fullPath));
    } else if (entry.name.endsWith('.mdx')) {
      files.push(fullPath);
    }
  }
  return files;
}

function toPosix(inputPath) {
  return inputPath.split(path.sep).join('/');
}

function getStatus(content, method) {
  const hasRequestSchema = /## Request body schema[\s\S]*?<CardGroup>/m.test(content);
  const hasResponseSchema = /## Response body schema[\s\S]*?<CardGroup>/m.test(content);

  if (method === 'GET') {
    return {
      expectedSchema: 'Response body schema',
      status: hasResponseSchema ? 'Present' : 'Missing',
    };
  }

  if (method === 'POST' || method === 'PUT') {
    return {
      expectedSchema: 'Request body schema',
      status: hasRequestSchema ? 'Present' : 'Missing',
    };
  }

  return {
    expectedSchema: 'Not tracked',
    status: 'Present',
  };
}

function main() {
  const rows = walk(MDX_ROOT)
    .filter((filePath) => path.basename(filePath) !== 'schema-status-report.md')
    .sort()
    .map((filePath) => {
      const content = fs.readFileSync(filePath, 'utf8');
      const openapiMatch = content.match(/^openapi:\s*'.*? (GET|POST|PUT|PATCH|DELETE) (.+?)'$/m);
      if (!openapiMatch) {
        return null;
      }

      const method = openapiMatch[1];
      const relativePath = toPosix(path.relative(MDX_ROOT, filePath));
      const { expectedSchema, status } = getStatus(content, method);

      return {
        method,
        file: `api-reference/gst/compliance/endpoints/taxpayer/${relativePath}`,
        expectedSchema,
        status,
      };
    })
    .filter(Boolean);

  const presentCount = rows.filter((row) => row.status === 'Present').length;
  const missingCount = rows.filter((row) => row.status === 'Missing').length;

  const lines = [
    '# Taxpayer API schema status',
    '',
    `Generated on: ${GENERATED_ON}`,
    '',
    'Scope: `api-reference/gst/compliance/endpoints/taxpayer/**/*.mdx`',
    '',
    'Status rule:',
    '- `POST` and `PUT` endpoints are `Present` only if the page contains a request body schema card inside a `CardGroup`.',
    '- `GET` endpoints are `Present` only if the page contains a response body schema card inside a `CardGroup`.',
    '',
    '## Summary',
    '',
    '| Metric | Count |',
    '| --- | ---: |',
    `| Total endpoint pages scanned | ${rows.length} |`,
    `| Present | ${presentCount} |`,
    `| Missing | ${missingCount} |`,
    '',
    '## API status',
    '',
    '| Method | File | Expected schema | Status |',
    '| --- | --- | --- | --- |',
  ];

  for (const row of rows) {
    lines.push(`| ${row.method} | \`${row.file}\` | ${row.expectedSchema} | ${row.status} |`);
  }

  fs.writeFileSync(OUTPUT_FILE, `${lines.join('\n')}\n`, 'utf8');
  console.log(`Wrote ${OUTPUT_FILE}`);
}

main();