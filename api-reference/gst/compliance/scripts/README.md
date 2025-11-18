# GSTN Schema Merger Scripts

This directory contains reusable scripts for merging GSTN response schemas into the OpenAPI specification.

## Overview

The `merge_gstn_schemas.py` script merges GSTN schema files into the OpenAPI file by updating the `data.data` properties for specific endpoints while preserving all existing examples.

## Features

- ✅ Merges GSTN schema properties into OpenAPI `data.data` objects
- ✅ Preserves all existing examples in the OpenAPI file
- ✅ Handles nested objects and arrays recursively
- ✅ Updates descriptions, titles, and required fields
- ✅ Supports single endpoint or batch processing
- ✅ Reusable for all GST compliance endpoints
- ✅ **Validates JSON schemas for duplicate keys and syntax errors before merging**

## Usage

### Single Endpoint

```bash
python merge_gstn_schemas.py \
  --openapi openapi.json \
  --endpoint "/gst/compliance/public/gstin/search" \
  --schema "../gstn-schemas/Search GSTIN - Response Schema.json"
```

### Batch Processing

Create a mappings file (see `mappings.example.json`) and run:

```bash
python merge_gstn_schemas.py \
  --openapi openapi.json \
  --batch mappings.json
```

### With Custom Output File

```bash
python merge_gstn_schemas.py \
  --openapi openapi.json \
  --endpoint "/gst/compliance/public/gstin/search" \
  --schema "../gstn-schemas/Search GSTIN - Response Schema.json" \
  --output updated_openapi.json
```

## Mappings File Format

The batch mappings file should be a JSON array with objects containing:

```json
[
  {
    "endpoint": "/gst/compliance/public/gstin/search",
    "schema_file": "../gstn-schemas/Search GSTIN - Response Schema.json",
    "method": "post"
  }
]
```

- `endpoint`: The API endpoint path (required)
- `schema_file`: Path to the GSTN schema JSON file (required)
- `method`: HTTP method (optional, default: "post")

## How It Works

1. **Loads OpenAPI file**: Reads the OpenAPI specification JSON file
2. **Finds endpoint**: Locates the endpoint in the `paths` section
3. **Navigates to schema**: Finds the response schema at `responses.200.content.application/json.schema`
4. **Locates data.data**: Navigates to `properties.data.properties.data`
5. **Merges schemas**: Merges GSTN schema properties into the existing schema:
   - Updates existing properties with descriptions/titles from GSTN schema
   - Adds missing properties from GSTN schema
   - Preserves all existing examples
   - Updates required fields
7. **Saves file**: Writes the updated OpenAPI file

## Merging Logic

- **Existing properties**: Updated with descriptions, titles, and type information from GSTN schema
- **New properties**: Added from GSTN schema
- **Examples**: Preserved from OpenAPI file (not overwritten)
- **Required fields**: Merged (GSTN required fields added to OpenAPI required list)
- **Nested objects**: Merged recursively
- **Arrays**: Items merged recursively

## Adding New Endpoints

To add a new endpoint:

1. Add the GSTN schema file to `../gstn-schemas/`
2. Add a mapping entry to your mappings file:
   ```json
   {
     "endpoint": "/gst/compliance/public/your-endpoint",
     "schema_file": "../gstn-schemas/Your Endpoint - Response Schema.json",
     "method": "post"
   }
   ```
3. Run the script with the batch file

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Notes

- The script modifies the OpenAPI file in place unless `--output` is specified
- Always backup your OpenAPI file before running the script
- The script preserves all examples, so you won't lose any existing example data
- Schema merging is additive - it won't remove properties that exist in OpenAPI but not in GSTN schema

