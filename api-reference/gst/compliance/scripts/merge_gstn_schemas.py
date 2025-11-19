#!/usr/bin/env python3
"""
Reusable script to merge GSTN schema files into OpenAPI specification.

This script merges GSTN response schemas into the OpenAPI file by updating
the data.data properties for specific endpoints while preserving all existing examples.

Usage:
    python merge_gstn_schemas.py --openapi <openapi_file> --endpoint <endpoint_path> --schema <gstn_schema_file>
    
    Or use the configuration file:
    python merge_gstn_schemas.py --config <config_file>
    
    Or process multiple endpoints:
    python merge_gstn_schemas.py --batch <mapping_file>
"""

import json
import argparse
import sys
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Set, Tuple
from copy import deepcopy


def validate_json_for_duplicates(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Validate JSON file for duplicate keys and syntax errors.
    
    Note: Python's json module silently overwrites duplicate keys, so we check
    the raw file content for duplicate keys in the same object level.
    
    Returns:
        (is_valid, error_message) tuple
    """
    try:
        # Read raw content to check for duplicate keys
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for duplicate keys in raw content (basic check)
        duplicates = find_duplicate_keys_in_raw_json(content)
        if duplicates:
            error_msg = f"Found duplicate keys in JSON file:\n"
            for line_num, keys in duplicates.items():
                error_msg += f"  Line {line_num}: {', '.join(keys)}\n"
            return False, error_msg
        
        # Parse JSON - this will catch syntax errors
        data = json.loads(content)
        
        # Also check parsed structure for logical duplicates in properties
        schema_duplicates = find_duplicate_keys_in_schema(data)
        if schema_duplicates:
            error_msg = f"Found duplicate keys in schema properties:\n"
            for path, keys in schema_duplicates.items():
                error_msg += f"  At {path}: {', '.join(keys)}\n"
            return False, error_msg
        
        return True, None
    except json.JSONDecodeError as e:
        return False, f"JSON syntax error: {str(e)}"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def find_duplicate_keys_in_raw_json(content: str) -> Dict[int, List[str]]:
    """
    Find duplicate keys in raw JSON content by using regex to find
    duplicate key patterns in the properties section.
    
    Returns:
        Dictionary mapping line numbers to lists of duplicate keys found
    """
    duplicates = {}
    lines = content.split('\n')
    
    # Find all "properties" objects and check for duplicate keys within them
    # This regex finds key-value pairs: "key": value
    key_pattern = re.compile(r'"([^"]+)":')
    
    # Track which lines are within a properties object
    in_properties = False
    properties_start_line = 0
    brace_depth = 0
    current_keys = {}  # Track keys seen in current properties object
    
    for line_num, line in enumerate(lines, 1):
        # Simple check: if line contains "properties" and opening brace, we're entering properties
        stripped = line.strip()
        if '"properties"' in stripped or "'properties'" in stripped:
            if '{' in stripped:
                in_properties = True
                properties_start_line = line_num
                current_keys = {}
                brace_depth = stripped.count('{') - stripped.count('}')
        
        if in_properties:
            # Count braces to track when we exit the properties object
            brace_depth += stripped.count('{') - stripped.count('}')
            
            # Find all keys in this line
            matches = key_pattern.findall(line)
            for key in matches:
                if key in current_keys:
                    # Duplicate found!
                    if line_num not in duplicates:
                        duplicates[line_num] = []
                    if key not in duplicates[line_num]:
                        duplicates[line_num].append(key)
                else:
                    current_keys[key] = line_num
            
            # Check if we've closed the properties object
            if brace_depth <= 0 and '}' in stripped:
                in_properties = False
                current_keys = {}
    
    return duplicates


def find_duplicate_keys_in_schema(schema: Dict[str, Any], path: str = "root") -> Dict[str, List[str]]:
    """
    Recursively find duplicate keys in schema properties.
    
    Returns:
        Dictionary mapping paths to lists of duplicate keys found
    """
    duplicates = {}
    
    if not isinstance(schema, dict):
        return duplicates
    
    # Check for duplicate keys in current level
    if 'properties' in schema and isinstance(schema['properties'], dict):
        seen_keys: Set[str] = set()
        duplicate_keys: List[str] = []
        
        for key in schema['properties'].keys():
            if key in seen_keys:
                duplicate_keys.append(key)
            else:
                seen_keys.add(key)
        
        if duplicate_keys:
            duplicates[path] = duplicate_keys
        
        # Recursively check nested properties
        for prop_name, prop_value in schema['properties'].items():
            if isinstance(prop_value, dict):
                nested_path = f"{path}.properties.{prop_name}"
                nested_duplicates = find_duplicate_keys_in_schema(prop_value, nested_path)
                duplicates.update(nested_duplicates)
    
    # Also check items in arrays
    if 'items' in schema and isinstance(schema['items'], dict):
        items_path = f"{path}.items"
        items_duplicates = find_duplicate_keys_in_schema(schema['items'], items_path)
        duplicates.update(items_duplicates)
    
    return duplicates


class GSTNSchemaMerger:
    """Handles merging GSTN schemas into OpenAPI specifications."""
    
    def __init__(self, openapi_file: str, dry_run: bool = False):
        """Initialize with OpenAPI file path."""
        self.openapi_file = Path(openapi_file)
        self.dry_run = dry_run
        if not self.openapi_file.exists():
            raise FileNotFoundError(f"OpenAPI file not found: {openapi_file}")
        
        with open(self.openapi_file, 'r', encoding='utf-8') as f:
            self.openapi_data = json.load(f)
        
        self.changes_log = []  # Track changes for dry-run output
    
    def find_endpoint(self, endpoint_path: str) -> Optional[Dict[str, Any]]:
        """Find endpoint in OpenAPI paths by path string."""
        paths = self.openapi_data.get('paths', {})
        if endpoint_path in paths:
            return paths[endpoint_path]
        return None
    
    def get_response_schema(self, endpoint: Dict[str, Any], method: str = 'post') -> Optional[Dict[str, Any]]:
        """Get the response schema for a specific method (default: post)."""
        if method not in endpoint:
            return None
        
        operation = endpoint[method]
        responses = operation.get('responses', {})
        response_200 = responses.get('200', {})
        content = response_200.get('content', {})
        json_content = content.get('application/json', {})
        return json_content.get('schema')
    
    def navigate_to_data_data(self, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Navigate to the data.data object in the response schema."""
        if not schema:
            return None
        
        properties = schema.get('properties', {})
        data = properties.get('data', {})
        if not data:
            return None
        
        data_properties = data.get('properties', {})
        inner_data = data_properties.get('data', {})
        
        return inner_data
    
    def merge_schema_properties(
        self, 
        target: Dict[str, Any], 
        source: Dict[str, Any],
        preserve_examples: bool = True,
        path: str = ""
    ) -> Dict[str, Any]:
        """
        Merge source schema properties into target, preserving examples.
        
        Args:
            target: Target schema object (data.data from OpenAPI)
            source: Source schema object (GSTN schema)
            preserve_examples: Whether to preserve existing examples in target
            path: Current path in schema for logging (used in dry-run)
        
        Returns:
            Merged schema object
        """
        if not target:
            target = {}
        
        if not source:
            return target
        
        # Get properties from source (GSTN schema)
        source_properties = source.get('properties', {})
        source_required = source.get('required', [])
        
        # Get or create properties in target
        if 'properties' not in target:
            target['properties'] = {}
        
        target_properties = target['properties']
        
        # Track changes for dry-run
        added_properties = []
        updated_properties = []
        
        # Merge each property from source
        for prop_name, prop_schema in source_properties.items():
            prop_path = f"{path}.{prop_name}" if path else prop_name
            if prop_name in target_properties:
                # Property exists - merge it recursively
                old_prop = deepcopy(target_properties[prop_name])
                target_properties[prop_name] = self._merge_property(
                    target_properties[prop_name],
                    prop_schema,
                    preserve_examples,
                    prop_path
                )
                updated_properties.append(prop_path)
            else:
                # New property - add it
                target_properties[prop_name] = deepcopy(prop_schema)
                added_properties.append(prop_path)
        
        # Log changes
        if self.dry_run:
            if added_properties:
                self.changes_log.append(f"  + Added properties: {', '.join(added_properties)}")
            if updated_properties:
                self.changes_log.append(f"  ~ Updated properties: {', '.join(updated_properties)}")
        
        # Update required fields
        if source_required:
            if 'required' not in target:
                target['required'] = []
            
            # Add missing required fields
            new_required = []
            for req_field in source_required:
                if req_field not in target['required']:
                    target['required'].append(req_field)
                    new_required.append(req_field)
            
            if self.dry_run and new_required:
                self.changes_log.append(f"  + Added to required: {', '.join(new_required)}")
        
        # Ensure type is set
        if 'type' not in target and source.get('type'):
            if self.dry_run:
                self.changes_log.append(f"  ~ Set type: {source.get('type')}")
            target['type'] = source.get('type')
        
        return target
    
    def _merge_property(
        self, 
        target_prop: Dict[str, Any], 
        source_prop: Dict[str, Any],
        preserve_examples: bool,
        path: str = ""
    ) -> Dict[str, Any]:
        """Merge a single property, preserving examples."""
        merged = deepcopy(target_prop)
        
        # Update type if source has it
        if 'type' in source_prop and merged.get('type') != source_prop['type']:
            if self.dry_run:
                self.changes_log.append(f"    {path}: type '{merged.get('type')}' -> '{source_prop['type']}'")
            merged['type'] = source_prop['type']
        
        # Update description if source has it
        if 'description' in source_prop:
            if 'description' not in merged or merged['description'] != source_prop['description']:
                if self.dry_run:
                    old_desc = merged.get('description', '(none)')
                    self.changes_log.append(f"    {path}: added/updated description")
                merged['description'] = source_prop['description']
        
        # Update title if source has it
        if 'title' in source_prop:
            if 'title' not in merged or merged['title'] != source_prop['title']:
                if self.dry_run:
                    self.changes_log.append(f"    {path}: added/updated title")
                merged['title'] = source_prop['title']
        
        # Handle nested objects
        if source_prop.get('type') == 'object' and 'properties' in source_prop:
            if 'properties' not in merged:
                merged['properties'] = {}
            
            for nested_prop_name, nested_prop_schema in source_prop['properties'].items():
                nested_path = f"{path}.{nested_prop_name}" if path else nested_prop_name
                if nested_prop_name in merged['properties']:
                    merged['properties'][nested_prop_name] = self._merge_property(
                        merged['properties'][nested_prop_name],
                        nested_prop_schema,
                        preserve_examples,
                        nested_path
                    )
                else:
                    merged['properties'][nested_prop_name] = deepcopy(nested_prop_schema)
                    if self.dry_run:
                        self.changes_log.append(f"    {nested_path}: added new property")
            
            # Merge required fields for nested objects
            if 'required' in source_prop:
                if 'required' not in merged:
                    merged['required'] = []
                new_required = []
                for req_field in source_prop['required']:
                    if req_field not in merged['required']:
                        merged['required'].append(req_field)
                        new_required.append(req_field)
                if self.dry_run and new_required:
                    self.changes_log.append(f"    {path}: added to required: {', '.join(new_required)}")
        
        # Handle arrays
        if source_prop.get('type') == 'array' and 'items' in source_prop:
            if 'items' not in merged:
                merged['items'] = {}
            
            items_path = f"{path}[items]"
            merged['items'] = self._merge_property(
                merged.get('items', {}),
                source_prop['items'],
                preserve_examples,
                items_path
            )
        
        # Preserve examples - don't overwrite if preserve_examples is True
        if preserve_examples:
            # Only add examples from source if target doesn't have them
            if 'example' not in merged and 'examples' in source_prop:
                # Convert examples array to single example if needed
                if isinstance(source_prop['examples'], list) and len(source_prop['examples']) > 0:
                    merged['example'] = source_prop['examples'][0]
                    if self.dry_run:
                        self.changes_log.append(f"    {path}: added example from GSTN schema")
            elif 'example' not in merged and 'example' in source_prop:
                merged['example'] = source_prop['example']
                if self.dry_run:
                    self.changes_log.append(f"    {path}: added example from GSTN schema")
        else:
            # Overwrite examples
            if 'examples' in source_prop:
                if isinstance(source_prop['examples'], list) and len(source_prop['examples']) > 0:
                    merged['example'] = source_prop['examples'][0]
            elif 'example' in source_prop:
                merged['example'] = source_prop['example']
        
        return merged
    
    def update_endpoint_schema(
        self, 
        endpoint_path: str, 
        gstn_schema_file: str,
        method: str = 'post'
    ) -> bool:
        """
        Update endpoint schema with GSTN schema.
        
        Args:
            endpoint_path: API endpoint path (e.g., '/gst/compliance/public/gstin/search')
            gstn_schema_file: Path to GSTN schema JSON file
            method: HTTP method (default: 'post')
        
        Returns:
            True if successful, False otherwise
        """
        # Load GSTN schema
        schema_path = Path(gstn_schema_file)
        if not schema_path.exists():
            print(f"Error: GSTN schema file not found: {gstn_schema_file}")
            return False
        
        # Validate JSON for duplicate keys and syntax errors
        is_valid, error_msg = validate_json_for_duplicates(schema_path)
        if not is_valid:
            print(f"Error: Invalid GSTN schema file: {gstn_schema_file}")
            print(error_msg)
            return False
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            gstn_schema = json.load(f)
        
        # Find endpoint
        endpoint = self.find_endpoint(endpoint_path)
        if not endpoint:
            print(f"Error: Endpoint not found: {endpoint_path}")
            return False
        
        # Get response schema
        response_schema = self.get_response_schema(endpoint, method)
        if not response_schema:
            print(f"Error: Response schema not found for {endpoint_path} ({method})")
            return False
        
        # Navigate to data.data
        data_data = self.navigate_to_data_data(response_schema)
        if not data_data:
            print(f"Error: data.data object not found in response schema for {endpoint_path}")
            return False
        
        # Clear changes log for this endpoint
        self.changes_log = []
        
        # Merge schemas
        mode_str = "[DRY RUN] " if self.dry_run else ""
        print(f"\n{mode_str}Merging GSTN schema into {endpoint_path}...")
        print(f"  Schema file: {gstn_schema_file}")
        
        # Create a copy for merging (don't modify original in dry-run)
        data_data_copy = deepcopy(data_data)
        merged_schema = self.merge_schema_properties(data_data_copy, gstn_schema, preserve_examples=True)
        
        # Show changes in dry-run mode
        if self.dry_run:
            if self.changes_log:
                print("  Changes that would be made:")
                for change in self.changes_log:
                    print(change)
            else:
                print("  No changes detected (schema already up to date)")
        else:
            # Update the schema in place
            response_schema['properties']['data']['properties']['data'] = merged_schema
            print(f"  ✓ Successfully merged schema")
        
        return True
    
    def save(self, output_file: Optional[str] = None):
        """Save the updated OpenAPI file."""
        if self.dry_run:
            print("\n[DRY RUN] File would be saved but dry-run mode is active.")
            return
        
        output_path = Path(output_file) if output_file else self.openapi_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.openapi_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved updated OpenAPI file to: {output_path}")


def load_config(config_file: str) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def process_single_mapping(
    openapi_file: str,
    endpoint_path: str,
    gstn_schema_file: str,
    method: str = 'post',
    output_file: Optional[str] = None,
    dry_run: bool = False
):
    """Process a single endpoint-schema mapping."""
    merger = GSTNSchemaMerger(openapi_file, dry_run=dry_run)
    success = merger.update_endpoint_schema(endpoint_path, gstn_schema_file, method)
    
    if success:
        merger.save(output_file)
    else:
        sys.exit(1)


def process_batch_mapping(
    mapping_file: str, 
    openapi_file: str, 
    output_file: Optional[str] = None,
    dry_run: bool = False
):
    """Process multiple endpoint-schema mappings from a file."""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mappings = json.load(f)
    
    merger = GSTNSchemaMerger(openapi_file, dry_run=dry_run)
    all_success = True
    
    for i, mapping in enumerate(mappings, 1):
        endpoint_path = mapping.get('endpoint')
        schema_file = mapping.get('schema_file')
        method = mapping.get('method', 'post')
        
        if not endpoint_path or not schema_file:
            print(f"Error: Invalid mapping #{i} - missing endpoint or schema_file")
            all_success = False
            continue
        
        success = merger.update_endpoint_schema(endpoint_path, schema_file, method)
        if not success:
            all_success = False
    
    if all_success:
        merger.save(output_file)
    else:
        print("\nSome mappings failed. OpenAPI file not saved.")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Merge GSTN schemas into OpenAPI specification',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single endpoint
  python merge_gstn_schemas.py \\
    --openapi openapi.json \\
    --endpoint "/gst/compliance/public/gstin/search" \\
    --schema "../gstn-schemas/Search GSTIN - Response Schema.json"
  
  # Batch processing
  python merge_gstn_schemas.py \\
    --openapi openapi.json \\
    --batch mappings.json
  
  # With output file
  python merge_gstn_schemas.py \\
    --openapi openapi.json \\
    --endpoint "/gst/compliance/public/gstin/search" \\
    --schema "../gstn-schemas/Search GSTIN - Response Schema.json" \\
    --output updated_openapi.json
        """
    )
    
    parser.add_argument(
        '--openapi',
        required=True,
        help='Path to OpenAPI JSON file'
    )
    
    parser.add_argument(
        '--endpoint',
        help='API endpoint path (e.g., /gst/compliance/public/gstin/search)'
    )
    
    parser.add_argument(
        '--schema',
        help='Path to GSTN schema JSON file'
    )
    
    parser.add_argument(
        '--method',
        default='post',
        choices=['get', 'post', 'put', 'patch', 'delete'],
        help='HTTP method (default: post)'
    )
    
    parser.add_argument(
        '--batch',
        help='Path to JSON file with batch mappings (see mappings.example.json)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (default: overwrites input file)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying the file'
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("=" * 70)
        print("DRY RUN MODE - No files will be modified")
        print("=" * 70)
    
    if args.batch:
        # Batch processing
        process_batch_mapping(args.batch, args.openapi, args.output, args.dry_run)
    elif args.endpoint and args.schema:
        # Single endpoint processing
        process_single_mapping(
            args.openapi,
            args.endpoint,
            args.schema,
            args.method,
            args.output,
            args.dry_run
        )
    else:
        parser.error("Either --batch or both --endpoint and --schema must be provided")
    
    if args.dry_run:
        print("\n" + "=" * 70)
        print("DRY RUN COMPLETE - No files were modified")
        print("Run without --dry-run to apply changes")
        print("=" * 70)


if __name__ == '__main__':
    main()

