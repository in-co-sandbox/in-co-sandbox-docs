/**
 * ============================================
 * OpenAPI Update Script - Modular Architecture
 * ============================================
 * 
 * This script synchronizes OpenAPI specification with Postman collection data.
 * 
 * STRUCTURE:
 * 1. Configuration - Define constants and custom rules
 * 2. Utility Functions - Helper functions for data extraction
 * 3. Main Processing Functions - Core business logic
 * 4. Main Execution - Orchestrates the entire process
 * 
 * HOW TO ADD NEW STEPS:
 * 1. Create a new function in the "MAIN PROCESSING FUNCTIONS" section
 * 2. Add the function call to the main() function in the desired order
 * 3. Pass necessary data between steps using return values
 * 
 * EXAMPLE:
 * function myNewStep(openapi, matches) {
 *     console.log('🔧 Running my new step...');
 *     // Your logic here
 *     return result;
 * }
 * 
 * Then in main():
 * const result = myNewStep(openapi, matches);
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ============================================
// CONFIGURATION
// ============================================

// Custom hardcoded status codes for custom HTTP exceptions
const CUSTOM_STATUS_CODES = {
    '422': '422 - Unprocessable Entity',
    '503': '503 - Source Unavailable',
    '521': '521 - Data Not Found',
    '523': '523 - Invalid Lifecycle'
};

const OPENAPI_PATH = './api-reference/kyc/openapi.json';
const POSTMAN_PATH = './api-reference/kyc/in-co-sandbox-kyc.postman_collection.json';

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Generate a random UUID v4
 */
function generateUUID() {
    return crypto.randomUUID();
}

/**
 * Get current timestamp in milliseconds
 */
function getCurrentTimestamp() {
    return Date.now();
}

/**
 * Read and parse JSON files
 */
function readFiles() {
    console.log('📂 Reading files...');
    const openapi = JSON.parse(fs.readFileSync(OPENAPI_PATH, 'utf8'));
    const postmanCollection = JSON.parse(fs.readFileSync(POSTMAN_PATH, 'utf8'));
    console.log('✓ Files loaded successfully\n');
    return { openapi, postmanCollection };
}

/**
 * Extract all paths and methods from OpenAPI specification
 */
function extractOpenapiPaths(openapi) {
    console.log('🔍 Extracting OpenAPI paths...');
    const openapiPaths = {};

    for (const [pathKey, pathValue] of Object.entries(openapi.paths)) {
        for (const [method, methodDetails] of Object.entries(pathValue)) {
            if (['get', 'post', 'put', 'patch', 'delete', 'options', 'head'].includes(method.toLowerCase())) {
                const key = `${method.toUpperCase()} ${pathKey}`;
                openapiPaths[key] = {
                    path: pathKey,
                    method: method.toUpperCase(),
                    details: methodDetails
                };
            }
        }
    }

    console.log(`✓ Found ${Object.keys(openapiPaths).length} OpenAPI paths\n`);
    return openapiPaths;
}

/**
 * Extract path from Postman URL object
 */
function extractPathFromPostmanUrl(urlObj) {
    if (!urlObj) return null;

    // If url.path exists, join it to create the path
    if (urlObj.path && Array.isArray(urlObj.path)) {
        return '/' + urlObj.path.join('/');
    }

    // Fallback: parse from raw URL
    if (urlObj.raw) {
        // Remove the host part
        let rawUrl = urlObj.raw;

        // Handle Postman variables like {{sandbox_host}}
        if (urlObj.host && Array.isArray(urlObj.host)) {
            const hostVar = urlObj.host.join('.');
            // Remove the host variable from the raw URL
            rawUrl = rawUrl.replace(new RegExp(`.*?${hostVar.replace(/[{}]/g, '\\$&')}`), '');
        } else if (typeof urlObj.host === 'string') {
            rawUrl = rawUrl.replace(new RegExp(`.*?${urlObj.host.replace(/[{}]/g, '\\$&')}`), '');
        } else {
            // Try to remove protocol and domain
            rawUrl = rawUrl.replace(/^https?:\/\/[^\/]+/, '');
        }

        // Extract path (remove query params)
        const pathMatch = rawUrl.match(/^([^?#]*)/);
        if (pathMatch) {
            return pathMatch[1] || '/';
        }
    }

    return null;
}

/**
 * Normalize path for comparison (replace Postman :param with OpenAPI {param})
 */
function normalizePath(pathStr) {
    // Convert :param to {param} for comparison
    return pathStr.replace(/:([^\/]+)/g, '{$1}');
}

/**
 * Recursively traverse Postman collection items to find matches
 */
function traversePostmanItems(items, openapiPaths, matches = []) {
    if (!items || !Array.isArray(items)) return matches;

    for (const item of items) {
        // Check if this item has a request
        if (item.request) {
            const method = item.request.method ? item.request.method.toUpperCase() : null;
            const postmanPath = extractPathFromPostmanUrl(item.request.url);

            if (method && postmanPath) {
                // Normalize the path for comparison
                const normalizedPath = normalizePath(postmanPath);
                const key = `${method} ${normalizedPath}`;

                // Check if this matches an OpenAPI path
                if (openapiPaths[key]) {
                    matches.push({
                        openapi: openapiPaths[key],
                        postman: item,
                        postmanPath: postmanPath,
                        normalizedPath: normalizedPath,
                        method: method
                    });
                }
            }
        }

        // Recursively traverse nested items
        if (item.item && Array.isArray(item.item)) {
            traversePostmanItems(item.item, openapiPaths, matches);
        }
    }

    return matches;
}

/**
 * Find matching paths between OpenAPI and Postman collection
 */
function findMatchingPaths(openapiPaths, postmanCollection) {
    console.log('🔗 Matching paths between OpenAPI and Postman...');
    const matches = traversePostmanItems(postmanCollection.item, openapiPaths);
    console.log(`✓ Found ${matches.length} matching paths\n`);
    return matches;
}

// ============================================
// MAIN PROCESSING FUNCTIONS
// ============================================

/**
 * Update OpenAPI response descriptions with Postman data
 */
function updateResponseDescriptions(openapi, matches) {
    console.log('✏️  Updating response descriptions...\n');
    console.log('===================================\n');

    let totalUpdates = 0;
    let updateDetails = [];

    matches.forEach((match, index) => {
        const { openapi: { path: openapiPath, method }, postman } = match;

        console.log(`\n--- Processing Match ${index + 1} ---`);
        console.log(`Path: ${method} ${openapiPath}`);

        // Get the OpenAPI method object
        const openapiMethod = openapi.paths[openapiPath][method.toLowerCase()];

        if (!openapiMethod || !openapiMethod.responses) {
            console.log(`  ⚠️  No responses found in OpenAPI for this path`);
            return;
        }

        // Get Postman responses
        const postmanResponses = postman.response || [];

        if (postmanResponses.length === 0) {
            console.log(`  ℹ️  No responses in Postman collection`);
            return;
        }

        console.log(`  Found ${postmanResponses.length} response(s) in Postman collection`);

        // For each Postman response, update the corresponding OpenAPI description
        postmanResponses.forEach((postmanResponse) => {
            const statusCode = postmanResponse.code?.toString();
            const status = postmanResponse.status || postmanResponse.name || '';

            if (!statusCode) {
                console.log(`    ⚠️  Postman response missing status code`);
                return;
            }

            // Check if this status code exists in OpenAPI
            if (openapiMethod.responses[statusCode]) {
                const oldDescription = openapiMethod.responses[statusCode].description || '';

                // Use custom hardcoded description if it's one of the custom status codes
                const newDescription = CUSTOM_STATUS_CODES[statusCode] || `${statusCode} - ${status}`;

                // Update the description
                openapiMethod.responses[statusCode].description = newDescription;

                const updateType = CUSTOM_STATUS_CODES[statusCode] ? '[CUSTOM]' : '';
                console.log(`    ✓ Updated ${statusCode} ${updateType}: "${oldDescription}" → "${newDescription}"`);
                totalUpdates++;
                updateDetails.push({
                    path: openapiPath,
                    method: method,
                    statusCode: statusCode,
                    oldDescription: oldDescription,
                    newDescription: newDescription,
                    isCustom: !!CUSTOM_STATUS_CODES[statusCode]
                });
            } else {
                console.log(`    ℹ️  Status code ${statusCode} not found in OpenAPI responses`);
            }
        });
    });

    return { totalUpdates, updateDetails };
}

/**
 * Inject response examples from Postman into OpenAPI specification
 */
function injectExamples(openapi, matches) {
    console.log('📝 Injecting response examples...\n');
    console.log('===================================\n');

    let totalExamples = 0;
    let exampleDetails = [];

    matches.forEach((match, index) => {
        const { openapi: { path: openapiPath, method }, postman } = match;

        console.log(`\n--- Processing Examples for Match ${index + 1} ---`);
        console.log(`Path: ${method} ${openapiPath}`);

        // Get the OpenAPI method object
        const openapiMethod = openapi.paths[openapiPath][method.toLowerCase()];

        if (!openapiMethod || !openapiMethod.responses) {
            console.log(`  ⚠️  No responses found in OpenAPI for this path`);
            return;
        }

        // Get Postman responses
        const postmanResponses = postman.response || [];

        if (postmanResponses.length === 0) {
            console.log(`  ℹ️  No responses in Postman collection`);
            return;
        }

        console.log(`  Found ${postmanResponses.length} response(s) in Postman collection`);

        // Track example names per status code to ensure uniqueness
        const exampleNamesByStatus = {};

        // For each Postman response, inject examples
        postmanResponses.forEach((postmanResponse, responseIndex) => {
            let statusCode = postmanResponse.code?.toString();
            const baseName = postmanResponse.name || `Example ${statusCode}`;
            const bodyString = postmanResponse.body;

            if (!statusCode) {
                console.log(`    ⚠️  Postman response missing status code`);
                return;
            }

            if (!bodyString) {
                console.log(`    ℹ️  No body found for ${baseName}`);
                return;
            }

            // Try to extract the actual status code from the response body for custom codes
            // This handles cases where Postman records 500 but the actual API returns 521, 523, etc.
            try {
                // First, do a quick check if the body contains a "code" field with a custom status
                const codeMatch = bodyString.match(/"code"\s*:\s*(\d+)/);
                if (codeMatch) {
                    const bodyCode = codeMatch[1];
                    // If it's a custom status code (521, 523) or matches our custom codes, use it
                    if (CUSTOM_STATUS_CODES[bodyCode] || ['521', '523'].includes(bodyCode)) {
                        statusCode = bodyCode;
                    }
                }
            } catch (e) {
                // If extraction fails, continue with the original statusCode
            }

            // Check if this status code exists in OpenAPI
            if (!openapiMethod.responses[statusCode]) {
                console.log(`    ℹ️  Status code ${statusCode} not found in OpenAPI responses - skipping`);
                return;
            }

            // Replace Postman dynamic variables with actual generated values
            let cleanedBody = bodyString;

            // Replace "{{$randomUUID}}" (already quoted) with actual UUIDs
            cleanedBody = cleanedBody.replace(/"\{\{\$randomUUID\}\}"/g, () => `"${generateUUID()}"`);

            // Replace "{{$guid}}" (already quoted) with actual GUIDs
            cleanedBody = cleanedBody.replace(/"\{\{\$guid\}\}"/g, () => `"${generateUUID()}"`);

            // Replace {{$timestamp}} with current timestamp (unquoted, usually followed by 000)
            cleanedBody = cleanedBody.replace(/\{\{\$timestamp\}\}/g, () => getCurrentTimestamp().toString().slice(0, -3));

            // Replace {{$randomInt}} with a random integer between 1000 and 9999
            cleanedBody = cleanedBody.replace(/\{\{\$randomInt\}\}/g, () => Math.floor(Math.random() * 9000 + 1000).toString());

            // Replace any remaining "{{variable}}" (quoted) patterns with sample string
            cleanedBody = cleanedBody.replace(/"\{\{[^}]+\}\}"/g, '"sample-value"');

            // Replace any remaining {{variable}} (unquoted) patterns with null
            cleanedBody = cleanedBody.replace(/\{\{[^}]+\}\}/g, 'null');

            // Parse the body string to JSON
            let bodyJson;
            try {
                bodyJson = JSON.parse(cleanedBody);
            } catch (e) {
                console.log(`    ⚠️  Failed to parse JSON for ${baseName}: ${e.message}`);
                return;
            }

            // Ensure the response has the correct structure
            if (!openapiMethod.responses[statusCode].content) {
                openapiMethod.responses[statusCode].content = {};
            }

            if (!openapiMethod.responses[statusCode].content['application/json']) {
                openapiMethod.responses[statusCode].content['application/json'] = {};
            }

            if (!openapiMethod.responses[statusCode].content['application/json'].examples) {
                openapiMethod.responses[statusCode].content['application/json'].examples = {};
            }

            // Ensure unique example name for this status code
            if (!exampleNamesByStatus[statusCode]) {
                exampleNamesByStatus[statusCode] = new Set();
            }

            let exampleName = baseName;
            let counter = 1;
            while (exampleNamesByStatus[statusCode].has(exampleName)) {
                exampleName = `${baseName} (${counter})`;
                counter++;
            }
            exampleNamesByStatus[statusCode].add(exampleName);

            // Inject the example
            openapiMethod.responses[statusCode].content['application/json'].examples[exampleName] = {
                value: bodyJson
            };

            console.log(`    ✓ Injected example "${exampleName}" for status ${statusCode}`);
            totalExamples++;
            exampleDetails.push({
                path: openapiPath,
                method: method,
                statusCode: statusCode,
                exampleName: exampleName
            });
        });
    });

    console.log(`\n✓ Total examples injected: ${totalExamples}\n`);
    return { totalExamples, exampleDetails };
}

/**
 * Save the updated OpenAPI specification to file
 */
function saveOpenapi(openapi, outputPath) {
    console.log(`\n💾 Saving updated OpenAPI to: ${outputPath}`);
    fs.writeFileSync(outputPath, JSON.stringify(openapi, null, 4));
    console.log('✓ File saved successfully\n');
}

/**
 * Print summary of updates
 */
function printSummary(matches, totalUpdates, updateDetails, totalExamples) {
    console.log('\n===================================');
    console.log('=== UPDATE SUMMARY ===');
    console.log('===================================');
    console.log(`Total paths matched: ${matches.length}`);
    console.log(`Total descriptions updated: ${totalUpdates}`);
    console.log(`Total examples injected: ${totalExamples}`);

    // Count custom status code updates
    const customUpdates = updateDetails.filter(d => d.isCustom);
    if (customUpdates.length > 0) {
        console.log(`\nCustom status codes applied: ${customUpdates.length}`);
        console.log(`  - 422 (Unprocessable Entity): ${customUpdates.filter(d => d.statusCode === '422').length}`);
        console.log(`  - 503 (Source Unavailable): ${customUpdates.filter(d => d.statusCode === '503').length}`);
        console.log(`  - 521 (Data Not Found): ${customUpdates.filter(d => d.statusCode === '521').length}`);
        console.log(`  - 523 (Invalid Lifecycle): ${customUpdates.filter(d => d.statusCode === '523').length}`);
    }
}

/**
 * Print detailed update log
 */
function printDetailedLog(updateDetails) {
    if (updateDetails.length === 0) return;

    console.log('\n=== Detailed Update Log ===');
    updateDetails.forEach((detail, idx) => {
        const customLabel = detail.isCustom ? ' [CUSTOM]' : '';
        console.log(`\n${idx + 1}. ${detail.method} ${detail.path}${customLabel}`);
        console.log(`   Status: ${detail.statusCode}`);
        console.log(`   Old: "${detail.oldDescription}"`);
        console.log(`   New: "${detail.newDescription}"`);
    });
}

// ============================================
// MAIN EXECUTION
// ============================================

/**
 * Main function to orchestrate the entire process
 * 
 * CURRENT PROCESSING STEPS:
 * ┌─────────────────────────────────────────┐
 * │ 1. Read Files                           │
 * │    - Load OpenAPI & Postman JSON        │
 * ├─────────────────────────────────────────┤
 * │ 2. Extract OpenAPI Paths                │
 * │    - Parse all endpoints & methods      │
 * ├─────────────────────────────────────────┤
 * │ 3. Find Matching Paths                  │
 * │    - Match OpenAPI ↔ Postman           │
 * ├─────────────────────────────────────────┤
 * │ 4. Update Response Descriptions         │
 * │    - Apply Postman descriptions         │
 * │    - Apply custom status codes          │
 * ├─────────────────────────────────────────┤
 * │ 5. Inject Response Examples             │
 * │    - Add Postman response bodies        │
 * │    - Parse & inject as JSON examples    │
 * ├─────────────────────────────────────────┤
 * │ 6. Save Updated OpenAPI                 │
 * │    - Write changes to file              │
 * ├─────────────────────────────────────────┤
 * │ 7. Print Summary                        │
 * │    - Show statistics                    │
 * ├─────────────────────────────────────────┤
 * │ 8. Print Detailed Log                   │
 * │    - Show all changes                   │
 * └─────────────────────────────────────────┘
 * 
 * To add a new step, create a function above and call it here.
 */
function main() {
    console.log('\n🚀 Starting OpenAPI Enrichment Process...\n');

    // Step 1: Read files
    const { openapi, postmanCollection } = readFiles();

    // Step 2: Extract OpenAPI paths
    const openapiPaths = extractOpenapiPaths(openapi);

    // Step 3: Find matching paths
    const matches = findMatchingPaths(openapiPaths, postmanCollection);

    // Step 4: Update response descriptions
    const { totalUpdates, updateDetails } = updateResponseDescriptions(openapi, matches);

    // Step 5: Inject response examples
    const { totalExamples, exampleDetails } = injectExamples(openapi, matches);

    // Step 6: Save updated OpenAPI
    saveOpenapi(openapi, OPENAPI_PATH);

    // Step 7: Print summary
    printSummary(matches, totalUpdates, updateDetails, totalExamples);

    // Step 8: Print detailed log
    printDetailedLog(updateDetails);

    console.log('\n✅ Process completed successfully!\n');
}

// Run the main function
main();


