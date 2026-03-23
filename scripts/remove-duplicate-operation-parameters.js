#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const WORKSPACE_ROOT = path.join(__dirname, '..');
const API_REFERENCE_DIR = path.join(WORKSPACE_ROOT, 'api-reference');
const OPENAPI_FILE_NAME = 'openapi.json';
const HTTP_METHODS = new Set(['get', 'post', 'put', 'patch', 'delete', 'options', 'head', 'trace']);

function parseArguments() {
  const args = process.argv.slice(2);
  const parsed = {
    targets: [],
    dryRun: false
  };

  for (let index = 0; index < args.length; index += 1) {
    const currentArg = args[index];
    const nextArg = args[index + 1];

    if (currentArg === '--openapi-spec' && nextArg) {
      parsed.targets.push(nextArg);
      index += 1;
      continue;
    }

    if (currentArg === '--dry-run') {
      parsed.dryRun = true;
      continue;
    }
  }

  return parsed;
}

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

function resolveTargetFiles(targets) {
  if (!targets || targets.length === 0) {
    return findOpenapiFiles(API_REFERENCE_DIR);
  }

  const resolved = [];

  for (const target of targets) {
    const absolutePath = path.isAbsolute(target)
      ? target
      : path.join(WORKSPACE_ROOT, target);

    if (!fs.existsSync(absolutePath)) {
      throw new Error(`Target path does not exist: ${target}`);
    }

    const stat = fs.statSync(absolutePath);

    if (stat.isDirectory()) {
      resolved.push(...findOpenapiFiles(absolutePath));
      continue;
    }

    if (stat.isFile()) {
      resolved.push(absolutePath);
    }
  }

  return Array.from(new Set(resolved));
}

function buildParameterKey(parameter) {
  if (!parameter || typeof parameter !== 'object') {
    return null;
  }

  if (typeof parameter.$ref === 'string' && parameter.$ref.length > 0) {
    return `ref:${parameter.$ref}`;
  }

  const paramIn = typeof parameter.in === 'string' ? parameter.in : null;
  const paramName = typeof parameter.name === 'string' ? parameter.name : null;

  if (!paramIn || !paramName) {
    return null;
  }

  return `in:${paramIn}|name:${paramName}`;
}

function removePathLevelParameterDuplicates(openapi) {
  const pathsObject = openapi && typeof openapi.paths === 'object' ? openapi.paths : {};
  let removedParameters = 0;
  let changedOperations = 0;

  for (const pathItem of Object.values(pathsObject)) {
    if (!pathItem || typeof pathItem !== 'object') {
      continue;
    }

    const pathParameters = Array.isArray(pathItem.parameters) ? pathItem.parameters : [];
    const pathParameterKeys = new Set(
      pathParameters
        .map(buildParameterKey)
        .filter((key) => key !== null)
    );

    if (pathParameterKeys.size === 0) {
      continue;
    }

    for (const [method, operation] of Object.entries(pathItem)) {
      if (!HTTP_METHODS.has(method) || !operation || typeof operation !== 'object') {
        continue;
      }

      if (!Array.isArray(operation.parameters) || operation.parameters.length === 0) {
        continue;
      }

      const previousCount = operation.parameters.length;
      operation.parameters = operation.parameters.filter((parameter) => {
        const key = buildParameterKey(parameter);
        return !(key && pathParameterKeys.has(key));
      });

      const removedInOperation = previousCount - operation.parameters.length;

      if (removedInOperation > 0) {
        changedOperations += 1;
        removedParameters += removedInOperation;
      }

      if (operation.parameters.length === 0) {
        delete operation.parameters;
      }
    }
  }

  return { removedParameters, changedOperations };
}

function processFile(filePath, dryRun) {
  const original = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  const { removedParameters, changedOperations } = removePathLevelParameterDuplicates(original);

  if (!dryRun && removedParameters > 0) {
    fs.writeFileSync(filePath, `${JSON.stringify(original, null, 2)}\n`, 'utf-8');
  }

  return { removedParameters, changedOperations };
}

function main() {
  const { targets, dryRun } = parseArguments();
  const targetFiles = resolveTargetFiles(targets);

  if (targetFiles.length === 0) {
    console.log('No OpenAPI files found.');
    return;
  }

  const modeText = dryRun ? 'DRY RUN' : 'WRITE';
  console.log(`🔍 Removing operation-level duplicate parameters (${modeText})...\n`);

  let changedFiles = 0;
  let totalRemoved = 0;
  let totalChangedOperations = 0;

  for (const filePath of targetFiles) {
    const { removedParameters, changedOperations } = processFile(filePath, dryRun);

    if (removedParameters === 0) {
      continue;
    }

    changedFiles += 1;
    totalRemoved += removedParameters;
    totalChangedOperations += changedOperations;

    console.log(
      `✅ ${path.relative(WORKSPACE_ROOT, filePath)}: removed ${removedParameters} duplicate parameters across ${changedOperations} operations`
    );
  }

  console.log(
    `\n✨ Done. ${dryRun ? 'Would update' : 'Updated'} ${changedFiles} files, ` +
    `removed ${totalRemoved} duplicate operation-level parameters from ${totalChangedOperations} operations.`
  );
}

main();