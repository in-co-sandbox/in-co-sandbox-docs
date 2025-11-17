import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import time
import xml.etree.ElementTree as ET
import re

# Load environment variables from root directory
script_dir = Path(__file__).parent
root_dir = script_dir.parent
load_dotenv(root_dir / '.env.local')

README_API_KEY = os.getenv('readme_api_key')
README_API_BASE = 'https://api.readme.com/v1'  # Using Legacy API v1

def get_project_info():
    """Get the project information from Readme API"""
    headers = {
        'Authorization': f'Bearer {README_API_KEY}'
    }
    response = requests.get(f'{README_API_BASE}/projects/me', headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data.get('data', {})
    else:
        print(f"Error getting project: {response.status_code} - {response.text}")
        return None

def get_branches():
    """Get all branches from Readme (v1 API)"""
    headers = {
        'Authorization': f'Bearer {README_API_KEY}',
        'accept': 'application/json'
    }
    # Try common branch names first
    common_branches = ['stable', 'main', 'master', 'production']
    for branch in common_branches:
        # Test if branch exists by trying to get a reference
        test_url = f'{README_API_BASE}/branches/{branch}/reference/test'
        response = requests.get(test_url, headers=headers)
        if response.status_code != 404:  # If not 404, branch might exist
            return [{'slug': branch}]
    
    # If no common branch works, try to get branches list (might not work in v1)
    response = requests.get(f'{README_API_BASE}/branches', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # Default to stable
        return [{'slug': 'stable'}]

def get_reference_page(branch, slug):
    """Get a reference page from Readme API v1"""
    headers = {
        'Authorization': f'Bearer {README_API_KEY}',
        'accept': 'application/json'
    }
    url = f'{README_API_BASE}/branches/{branch}/reference/{slug}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        # Don't print error for 403/404, just return None
        if response.status_code not in [403, 404]:
            print(f"Error getting reference {slug}: {response.status_code}")
        return None

def parse_readme_sitemap(sitemap_path):
    """Parse the Readme sitemap XML and extract reference page slugs"""
    slug_map = {}
    
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        # Define namespace
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        for url in root.findall('.//ns:url', ns):
            loc = url.find('ns:loc', ns)
            if loc is not None and loc.text:
                url_text = loc.text
                # Extract reference slug from URL
                match = re.search(r'/reference/([^/]+)$', url_text)
                if match:
                    slug = match.group(1)
                    # Store the full URL for potential use
                    slug_map[slug] = url_text
                    
        print(f"Parsed {len(slug_map)} reference pages from sitemap")
        return slug_map
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
        return {}

def load_path_to_slug_mapping():
    """Load the direct path to slug mapping"""
    mapping_path = root_dir / 'scripts/path_to_slug_mapping.json'
    try:
        with open(mapping_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Mapping file not found at {mapping_path}")
        return {}

def map_endpoint_to_readme_slug(api_key, path, path_to_slug_map, sitemap_slugs):
    """Map API endpoint path to Readme reference slug using direct mapping"""
    # Try exact match with method and path first (e.g., "POST /gst/compliance/...")
    if api_key in path_to_slug_map:
        slug = path_to_slug_map[api_key]
        if slug in sitemap_slugs:
            return [slug]
        else:
            print(f"  ⚠ Slug '{slug}' from mapping not found in sitemap for {api_key}")
    
    # Try exact path match (without method)
    if path in path_to_slug_map:
        slug = path_to_slug_map[path]
        if slug in sitemap_slugs:
            return [slug]
    
    # Try with path parameters removed
    path_without_params = path
    for param in ['{year}', '{month}', '{irn}', '{ewb_no}', '{consolidated_ewb_no}', '{gstr}', '{din}']:
        path_without_params = path_without_params.replace(f'/{param}', '').replace(param, '')
    
    # Try matching patterns in mapping (check both with and without method)
    for mapped_key, slug in path_to_slug_map.items():
        # Extract path from mapped_key if it includes method
        mapped_path = mapped_key.split()[-1] if ' ' in mapped_key else mapped_key
        
        mapped_path_clean = mapped_path
        for param in ['{year}', '{month}', '{irn}', '{ewb_no}', '{consolidated_ewb_no}', '{gstr}', '{din}']:
            mapped_path_clean = mapped_path_clean.replace(f'/{param}', '').replace(param, '')
        
        if path_without_params == mapped_path_clean:
            if slug in sitemap_slugs:
                return [slug]
    
    # Fallback: try to generate slug from path
    clean_path = path.replace('/gst/compliance/', '').replace('/{year}', '').replace('/{month}', '')
    clean_path = clean_path.replace('/{irn}', '').replace('/{ewb_no}', '').replace('/{consolidated_ewb_no}', '')
    clean_path = clean_path.replace('/{gstr}', '').replace('/{din}', '').replace('/', '-').lower()
    clean_path = clean_path.replace('tax-payer', 'taxpayer')
    
    # Generate a few variations
    variations = [
        clean_path,
        clean_path + '-api',
        clean_path.replace('-api', '') + '-api'
    ]
    
    # Return only variations that exist in sitemap
    valid_variations = [v for v in variations if v in sitemap_slugs]
    return valid_variations if valid_variations else variations[:3]

def update_endpoint_file(file_path, description):
    """Update the description in an endpoint MDX file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2] if len(parts) > 2 else ''
                
                # Update description in frontmatter
                lines = frontmatter.strip().split('\n')
                updated_lines = []
                description_updated = False
                
                for line in lines:
                    if line.startswith('description:'):
                        # Escape quotes in description
                        escaped_desc = description.replace('"', '\\"').replace('\n', ' ')
                        updated_lines.append(f'description: "{escaped_desc}"')
                        description_updated = True
                    else:
                        updated_lines.append(line)
                
                if not description_updated:
                    # Add description if it doesn't exist
                    updated_lines.append(f'description: "{description}"')
                
                new_content = '---\n' + '\n'.join(updated_lines) + '\n---' + body
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False
    
    return False

def main():
    print("Using Readme API v1 (Legacy)...")
    
    # Get branches - try common ones
    branches = get_branches()
    if not branches:
        print("Could not get branches. Using default 'stable'...")
        branch = 'stable'
    else:
        # Use the first branch
        branch = branches[0].get('slug', 'stable') if isinstance(branches, list) and len(branches) > 0 else 'stable'
    
    print(f"Using branch: {branch}")
    
    # Parse sitemap to get correct slugs
    sitemap_path = root_dir / 'api-reference/readme_sitemap.xml'
    print("Parsing Readme sitemap...")
    sitemap_slugs = parse_readme_sitemap(sitemap_path)
    
    # Load path to slug mapping
    print("Loading path to slug mapping...")
    path_to_slug_map = load_path_to_slug_mapping()
    print(f"Loaded {len(path_to_slug_map)} path mappings")
    
    # Load OpenAPI spec to get all endpoints
    openapi_path = root_dir / 'api-reference/gst/compliance/openapi.json'
    with open(openapi_path, encoding='utf-8') as f:
        spec_data = json.load(f)
    
    paths = spec_data['paths']
    gst_paths = {p: paths[p] for p in paths.keys() if p.startswith('/gst/compliance/')}
    
    print(f"\nFound {len(gst_paths)} GST compliance endpoints")
    print("Fetching descriptions from Readme API...\n")
    
    # Find all MDX files
    endpoints_dir = root_dir / 'api-reference/gst/compliance/endpoints'
    mdx_files = list(endpoints_dir.rglob('*.mdx'))
    
    print(f"Found {len(mdx_files)} endpoint files")
    
    updated_count = 0
    not_found_count = 0
    
    for mdx_file in mdx_files:
        # Read the file to get the endpoint path
        try:
            with open(mdx_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract endpoint path from openapi line
            openapi_line = None
            for line in content.split('\n'):
                if line.startswith('openapi:'):
                    openapi_line = line
                    break
            
            if not openapi_line:
                print(f"  ⚠ No openapi line found in {mdx_file}")
                continue
            
            # Extract path from openapi line: 'openapi: '../../openapi.json POST /gst/compliance/...'
            parts = openapi_line.split()
            if len(parts) >= 3:
                method = parts[-2]
                endpoint_path = parts[-1].strip("'\"")  # Strip quotes from path
                
                # Create key with method and path for exact matching
                api_key = f"{method.upper()} {endpoint_path}"
                
                # Show which file we're processing
                file_name = mdx_file.name if hasattr(mdx_file, 'name') else str(mdx_file).split('/')[-1]
                print(f"Processing {file_name}...", end=' ')
                
                # Get Readme slug variations using direct mapping and sitemap
                readme_slug_variations = map_endpoint_to_readme_slug(api_key, endpoint_path, path_to_slug_map, sitemap_slugs)
                
                # Try each variation until one works
                reference = None
                used_slug = None
                for slug_variant in readme_slug_variations:
                    reference = get_reference_page(branch, slug_variant)
                    if reference:
                        used_slug = slug_variant
                        break
                
                if reference:
                    # Extract description from v1 API response
                    # v1 API might have different structure
                    description = None
                    if isinstance(reference, dict):
                        description = reference.get('body', '').strip()
                        if not description:
                            description = reference.get('bodyContent', '').strip()
                        if not description:
                            description = reference.get('excerpt', '').strip()
                    if not description:
                        description = reference.get('title', '').strip()
                    
                    if description:
                        # Update the file
                        if update_endpoint_file(mdx_file, description):
                            print(f"[OK] Updated (slug: {used_slug})")
                            updated_count += 1
                        else:
                            print(f"[FAIL] Failed to update")
                    else:
                        print(f"[WARN] No description found in response")
                else:
                    print(f"[NOT FOUND] Tried: {', '.join(readme_slug_variations[:2])}...")
                    not_found_count += 1
                
                # Rate limiting - be nice to the API
                time.sleep(0.5)
        except Exception as e:
            print(f"  [ERROR] Error processing {mdx_file}: {e}")
    
    print(f"\n[SUMMARY] Updated {updated_count} files")
    print(f"[SUMMARY] {not_found_count} endpoints not found in Readme")
    print("Done!")

if __name__ == '__main__':
    main()

