#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const WORKSPACE_ROOT = path.join(__dirname, '..');
const API_REFERENCE_DIR = path.join(WORKSPACE_ROOT, 'api-reference');
const OPENAPI_FILE_NAME = 'openapi.json';
const TRACE_HEADER_NAME = 'X-Amzn-Trace-Id';

function findOpenapiFiles(dirPath) {
  const openapiFiles = [];

  for (const entry of fs.readdirSync(dirPath, { withFileTypes: true })) {
    const fullPath = path.join(dirPath, entry.name);

    if (entry.isDirectory()) {
      openapiFiles.push(...findOpenapiFiles(fullPath));
      continue;
    }

    if (entry.isFile() && entry.name === OPENAPI_FILE_NAME) {
      openapiFiles.push(fullPath);
    }
  }

  return openapiFiles;
}

function shouldRemoveResponseHeaders(headers) {
  return Boolean(headers && typeof headers === 'object' && TRACE_HEADER_NAME in headers);
}

function stripResponseHeadersFromOpenapi(filePath) {
  const openapi = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  let removedResponseHeaders = 0;

  for (const pathItem of Object.values(openapi.paths || {})) {
    if (!pathItem || typeof pathItem !== 'object') {
      continue;
    }

    for (const [method, operation] of Object.entries(pathItem)) {
      if (method === 'parameters' || !operation || typeof operation !== 'object') {
        continue;
      }

      const responses = operation.responses && typeof operation.responses === 'object'
        ? operation.responses
        : {};

      for (const response of Object.values(responses)) {
        if (!response || typeof response !== 'object' || !shouldRemoveResponseHeaders(response.headers)) {
          continue;
        }

        delete response.headers;
        removedResponseHeaders += 1;
      }
    }
  }

  if (removedResponseHeaders > 0) {
    fs.writeFileSync(filePath, `${JSON.stringify(openapi, null, 2)}\n`, 'utf-8');
  }

  return removedResponseHeaders;
}

function main() {
  console.log('🚀 Stripping traced response headers from OpenAPI specs...\n');

  const openapiFiles = findOpenapiFiles(API_REFERENCE_DIR);
  let changedFiles = 0;
  let removedResponseHeaders = 0;

  for (const filePath of openapiFiles) {
    const removedInFile = stripResponseHeadersFromOpenapi(filePath);

    if (removedInFile === 0) {
      continue;
    }

    changedFiles += 1;
    removedResponseHeaders += removedInFile;

    console.log(`✅ ${path.relative(WORKSPACE_ROOT, filePath)}: removed ${removedInFile} response.headers blocks`);
  }

  console.log(`\n✨ Done. Updated ${changedFiles} OpenAPI files and removed ${removedResponseHeaders} response.headers blocks.`);
}

main();