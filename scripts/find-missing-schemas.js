const fs = require('fs');
const path = require('path');

const spec = JSON.parse(fs.readFileSync('api-reference/gst/compliance/openapi.json', 'utf8'));
const mdxDir = 'api-reference/gst/compliance/endpoints/taxpayer';

function walk(dir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...walk(full));
    else if (entry.name.endsWith('.mdx')) files.push(full);
  }
  return files;
}

const mdxFiles = walk(mdxDir);
const results = [];

for (const f of mdxFiles) {
  const content = fs.readFileSync(f, 'utf8');
  const openapiMatch = content.match(/^openapi:\s*'.*? (GET|POST|PUT|PATCH|DELETE) (.+?)'/m);
  const titleMatch = content.match(/^title:\s*['"](.+?)['"]/m);
  if (!openapiMatch) continue;
  const method = openapiMatch[1];
  const apiPath = openapiMatch[2].trim();
  const title = titleMatch ? titleMatch[1] : '';
  const hasCardGroup = content.indexOf('CardGroup') !== -1;

  if (method === 'GET' && !hasCardGroup) {
    // Check if OpenAPI spec has a response schema
    const specEntry = spec.paths[apiPath];
    const methodEntry = specEntry && specEntry[method.toLowerCase()];
    const hasResponseSchema = !!(
      methodEntry &&
      methodEntry.responses &&
      methodEntry.responses['200'] &&
      methodEntry.responses['200'].content &&
      methodEntry.responses['200'].content['application/json'] &&
      methodEntry.responses['200'].content['application/json'].schema
    );

    const relativePath = f.replace(/\\/g, '/').split('api-reference/gst/compliance/endpoints/taxpayer/')[1];
    results.push({ file: relativePath, method, apiPath, title, hasResponseSchema: hasResponseSchema ? 'Yes' : 'No' });
  }
}

console.log('| File | Method | API Path | Title | Response Schema in OpenAPI |');
console.log('|------|--------|----------|-------|---------------------------|');
results.forEach(function(r) {
  process.stdout.write('| ' + r.file + ' | ' + r.method + ' | `' + r.apiPath + '` | ' + r.title + ' | ' + r.hasResponseSchema + ' |\n');
});
console.log('\nTotal GET without CardGroup:', results.length);
console.log('Missing response schema in OpenAPI:', results.filter(function(r) { return r.hasResponseSchema === 'No'; }).length);
