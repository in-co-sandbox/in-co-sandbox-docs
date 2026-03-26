#!/usr/bin/env node

/**
 * add-example-summaries.js
 *
 * For every response example in an OpenAPI spec:
 * - If the example has a `summary` field, rename the key to the summary value
 *   (e.g. key "1" with summary "Success" becomes key "Success").
 * - If the example has no `summary`, add one equal to the current key name.
 *
 * Scope: responses.{status}.content.{media}.examples.{key}
 *
 * Usage:
 *   node scripts/add-example-summaries.js --openapi-spec <path>
 *
 * Example:
 *   node scripts/add-example-summaries.js \
 *     --openapi-spec ./api-reference/kyc/openapi.json
 */

const fs = require('fs');

function parseArguments() {
    const args = process.argv.slice(2);
    let openapiPath = null;

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--openapi-spec' && args[i + 1]) {
            openapiPath = args[i + 1];
            i++;
        }
    }

    if (!openapiPath) {
        console.error('❌ Missing required argument: --openapi-spec');
        console.error('\nUsage:');
        console.error('  node scripts/add-example-summaries.js --openapi-spec <path>');
        process.exit(1);
    }

    if (!fs.existsSync(openapiPath)) {
        console.error(`❌ File not found: ${openapiPath}`);
        process.exit(1);
    }

    return openapiPath;
}

function processExamples(openapi) {
    let renamed = 0;
    let summaryAdded = 0;

    const HTTP_METHODS = ['get', 'post', 'put', 'patch', 'delete', 'options', 'head'];

    for (const [pathKey, pathItem] of Object.entries(openapi.paths || {})) {
        for (const [method, operation] of Object.entries(pathItem)) {
            if (!HTTP_METHODS.includes(method)) continue;
            if (!operation || typeof operation !== 'object') continue;

            for (const [statusCode, response] of Object.entries(operation.responses || {})) {
                for (const [mediaType, mediaObject] of Object.entries(response.content || {})) {
                    const examples = mediaObject.examples;
                    if (!examples || typeof examples !== 'object') continue;

                    // Build a new examples object with keys replaced by summary values
                    const updated = {};
                    for (const [exampleKey, exampleObject] of Object.entries(examples)) {
                        if (!exampleObject || typeof exampleObject !== 'object') {
                            updated[exampleKey] = exampleObject;
                            continue;
                        }

                        if ('summary' in exampleObject) {
                            const newKey = exampleObject.summary;
                            if (newKey !== exampleKey) {
                                updated[newKey] = exampleObject;
                                console.log(`  ✓ Renamed key "${exampleKey}" → "${newKey}"  [${method.toUpperCase()} ${pathKey} ${statusCode}]`);
                                renamed++;
                            } else {
                                updated[exampleKey] = exampleObject;
                            }
                        } else {
                            // No summary — add one equal to the key name
                            updated[exampleKey] = { summary: exampleKey, ...exampleObject };
                            console.log(`  + Added summary "${exampleKey}"  [${method.toUpperCase()} ${pathKey} ${statusCode}]`);
                            summaryAdded++;
                        }
                    }

                    mediaObject.examples = updated;
                }
            }
        }
    }

    return { renamed, summaryAdded };
}

function main() {
    const openapiPath = parseArguments();

    console.log(`\n📂 Reading: ${openapiPath}`);
    const openapi = JSON.parse(fs.readFileSync(openapiPath, 'utf8'));

    console.log('\n📝 Processing examples...\n');
    const { renamed, summaryAdded } = processExamples(openapi);

    fs.writeFileSync(openapiPath, JSON.stringify(openapi, null, 2) + '\n', 'utf8');

    console.log(`\n✅ Done.`);
    console.log(`   Keys renamed to summary value: ${renamed}`);
    console.log(`   Summaries added (key had none): ${summaryAdded}\n`);
}

main();
