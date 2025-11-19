const fs = require('fs');
const path = require('path');

// CONFIGURATION
const INPUT_FILE = 'input.json';
const OUTPUT_FILE = 'output.md';

/**
 * Helper: Clean cell content for MDX/Mintlify
 */
function cleanCellContent(val) {
    if (!val) return '';
    if (typeof val !== 'string') return String(val);

    let content = val;

    // 1. Fix Newlines for MDX (must be self-closing <br />)
    content = content.replace(/\n/g, '<br />');

    // 2. Fix ReadMe Angle-Bracket URLs (<https://...>) 
    // MDX treats these as broken HTML tags. We strip the < >.
    content = content.replace(/<(https?:\/\/[^>]+)>/g, '$1');

    // 3. Fix Escaped Colons in URLs (https\:// -> https://)
    content = content.replace(/(https?)\\%3A\/\//g, '$1://'); // if URL encoded
    content = content.replace(/(https?)\\:\/\//g, '$1://');   // if backslash escaped

    // 4. Escape Pipes (|) so the table structure doesn't break
    content = content.replace(/\|/g, '\\|');

    return content;
}

function generateTableFromData(data, rows, cols) {
    let mdTable = '\n';

    // 1. Build Headers
    const headerCells = [];
    const dividerCells = [];

    for (let c = 0; c < cols; c++) {
        const headerKey = `h-${c}`;
        const headerVal = data[headerKey] || '';
        headerCells.push(cleanCellContent(headerVal));
        dividerCells.push('---');
    }
    mdTable += `| ${headerCells.join(' | ')} |\n`;
    mdTable += `| ${dividerCells.join(' | ')} |\n`;

    // 2. Build Rows
    for (let r = 0; r < rows; r++) {
        const rowCells = [];
        for (let c = 0; c < cols; c++) {
            const cellKey = `${r}-${c}`;
            let cellVal = data[cellKey] || '';

            // Clean the content using our helper function
            cellVal = cleanCellContent(cellVal);

            rowCells.push(cellVal);
        }
        mdTable += `| ${rowCells.join(' | ')} |\n`;
    }

    return mdTable + '\n';
}

function processJsonToMarkdown() {
    try {
        const rawData = fs.readFileSync(INPUT_FILE, 'utf8');
        let content;

        try {
            content = JSON.parse(rawData);
        } catch (e) {
            console.error("Error: The input file is not valid JSON.");
            return;
        }

        let finalMarkdown = "";

        // Handle "data" object structure
        if (content.data && content.cols && content.rows) {
            finalMarkdown += generateTableFromData(content.data, content.rows, content.cols);
        }
        // Handle ReadMe page body export
        else if (content.body) {
            const regex = /\[block:parameters\]([\s\S]*?)\[\/block\]/g;
            finalMarkdown = content.body.replace(regex, (match, jsonString) => {
                try {
                    const tableJson = JSON.parse(jsonString);
                    return generateTableFromData(tableJson.data, tableJson.rows, tableJson.cols);
                } catch (e) {
                    return match;
                }
            });
        }
        // Handle raw JSON paste
        else {
            if (content.data) {
                finalMarkdown = generateTableFromData(content.data, content.rows, content.cols);
            } else {
                console.log("Unknown JSON structure.");
            }
        }

        fs.writeFileSync(OUTPUT_FILE, finalMarkdown, 'utf8');
        console.log(`\nSuccess! Converted content written to ${OUTPUT_FILE}`);

    } catch (err) {
        console.error("Error processing file:", err);
    }
}

processJsonToMarkdown();