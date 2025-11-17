import json
import xml.etree.ElementTree as ET
import re
from pathlib import Path

def parse_sitemap_slugs():
    """Parse sitemap and extract all reference slugs"""
    tree = ET.parse('api-reference/readme_sitemap.xml')
    root = tree.getroot()
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    slugs = {}
    for url in root.findall('.//ns:url', ns):
        loc = url.find('ns:loc', ns)
        if loc is not None and loc.text:
            match = re.search(r'/reference/([^/]+)$', loc.text)
            if match:
                slug = match.group(1)
                slugs[slug] = loc.text
    
    return slugs

def get_all_api_paths():
    """Get all API paths from OpenAPI spec"""
    with open('api-reference/gst/compliance/openapi.json', encoding='utf-8') as f:
        spec = json.load(f)
    
    paths = {}
    for path, methods in spec['paths'].items():
        if path.startswith('/gst/compliance/'):
            for method, details in methods.items():
                if method.lower() in ['get', 'post', 'put', 'patch', 'delete']:
                    key = f"{method.upper()} {path}"
                    paths[key] = {
                        'path': path,
                        'method': method.upper(),
                        'summary': details.get('summary', ''),
                        'tags': details.get('tags', [])
                    }
    
    return paths

def normalize_path_for_matching(path):
    """Normalize path by removing path parameters for matching"""
    # Remove path parameters like {year}, {month}, etc.
    normalized = re.sub(r'/\{[^}]+\}', '', path)
    normalized = re.sub(r'\{[^}]+\}', '', normalized)
    return normalized

def create_mapping():
    """Create mapping from API paths to Readme slugs"""
    sitemap_slugs = parse_sitemap_slugs()
    api_paths = get_all_api_paths()
    
    print(f"Found {len(sitemap_slugs)} slugs in sitemap")
    print(f"Found {len(api_paths)} API endpoints")
    
    # Filter GST-related slugs
    gst_slugs = {k: v for k, v in sitemap_slugs.items() 
                 if any(x in k.lower() for x in ['gst', 'taxpayer', 'einvoice', 'eway', 'gstr', 'invoice', 'ledger', 'evc'])}
    
    print(f"Found {len(gst_slugs)} GST-related slugs")
    
    # Create mapping
    mapping = {}
    
    # Direct path mappings (manually curated based on sitemap)
    direct_mappings = {
        # Public APIs
        'POST /gst/compliance/public/gstin/search': 'search-gstin-api',
        'POST /gst/compliance/public/pan/search': 'search-gstin-by-pan-api',
        'POST /gst/compliance/public/gstrs/track': 'track-gst-returns-api',
        
        # Taxpayer Authentication
        'POST /gst/compliance/tax-payer/authenticate': 'gst-taxpayer-authentication',
        'POST /gst/compliance/tax-payer/otp': 'taxpayer-generate-otp-api',
        'POST /gst/compliance/tax-payer/otp/verify': 'taxpayer-verify-otp-api',
        'POST /gst/compliance/tax-payer/session/refresh': 'taxpayer-refresh-access-token-api',
        'POST /gst/compliance/tax-payer/logout': 'taxpayer-logout-api',
        'POST /gst/compliance/tax-payer/evc/otp': 'generate-evc-otp-api',
        
        # GSTR-1 APIs
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/at/{year}/{month}': 'gstr-1-at-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/ata/{year}/{month}': 'gstr-1-ata-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/b2b/{year}/{month}': 'gstr-1-b2b-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/b2ba/{year}/{month}': 'gstr-1-b2ba-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/b2cl/{year}/{month}': 'gstr-1-b2cl-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/b2cla/{year}/{month}': 'gstr-1-b2cla-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/b2cs/{year}/{month}': 'gstr-1-b2cs-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/b2csa/{year}/{month}': 'gstr-1-b2csa-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/cdnr/{year}/{month}': 'gstr-1-cdnr-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/cdnra/{year}/{month}': 'gstr-1-cdnra-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/cdnur/{year}/{month}': 'gstr-1-cdnur-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/cdnura/{year}/{month}': 'gstr-1-cdnura-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/doc-issue/{year}/{month}': 'gstr-1-document-issued-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/exp/{year}/{month}': 'gstr-1-exp-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/expa/{year}/{month}': 'gstr-1-expa-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/nil/{year}/{month}': 'gstr-1-nil-supplies-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/hsn/{year}/{month}': 'gstr-1-hsn-summary-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-1/{year}/{month}': 'gstr-1-summary-api',
        'POST /gst/compliance/tax-payer/gstrs/gstr-1/{year}/{month}': 'save-gstr-1-api',
        'POST /gst/compliance/tax-payer/gstrs/gstr-1/{year}/{month}/file': 'file-gstr-1-api',
        'POST /gst/compliance/tax-payer/gstrs/gstr-1/{year}/{month}/reset': 'reset-gstr-1-api',
        'POST /gst/compliance/tax-payer/gstrs/{gstr}/{year}/{month}/proceed': 'proceed-to-file-api',
        'POST /gst/compliance/tax-payer/gstrs/{gstr}/{year}/{month}/new-proceed': 'new-proceed-to-file-api',
        
        # GSTR-2A APIs
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/amdhist/{year}/{month}': 'gstr-2a-amdhist',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/b2b/{year}/{month}': 'gstr-2a-b2b-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/b2ba/{year}/{month}': 'gstr-2a-b2ba-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/cdn/{year}/{month}': 'gstr-2a-cdn-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/cdna/{year}/{month}': 'gstr-2a-cdna-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/impg/{year}/{month}': 'gstr-2a-impg',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/impgsez/{year}/{month}': 'gstr-2a-impgsez',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/isd/{year}/{month}': 'gstr-2a-isd-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/tcs/{year}/{month}': 'gstr-2a-tcs',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/tds/{year}/{month}': 'gstr-2a-tds',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2a/{year}/{month}': 'gstr-2a-api',
        
        # GSTR-2B APIs
        'GET /gst/compliance/tax-payer/gstrs/gstr-2b/{year}/{month}': 'gstr-2b-api',
        'POST /gst/compliance/tax-payer/gstrs/gstr-2b/regenerate': 'regenerate-gstr-2b',
        'GET /gst/compliance/tax-payer/gstrs/gstr-2b/{year}/{month}/regenerate': 'gstr-2b-regeneration-status',
        
        # GSTR-3B APIs
        'GET /gst/compliance/tax-payer/gstrs/gstr-3b/{year}/{month}': 'gstr-3b-details-api',
        'POST /gst/compliance/tax-payer/gstrs/gstr-3b/{year}/{month}': 'save-gstr-3b-api',
        'POST /gst/compliance/tax-payer/gstrs/gstr-3b/{year}/{month}/file': 'file-gstr-3b-api',
        'POST /gst/compliance/tax-payer/gstrs/gstr-3b/{year}/{month}/offset-liability': 'gstr-3b-offset-liability',
        
        # GSTR-9 APIs
        'GET /gst/compliance/tax-payer/gstrs/gstr-9': 'gstr-9-get-details-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-9/auto-calculated': 'gstr-9-auto-calculated-details-api',
        'GET /gst/compliance/tax-payer/gstrs/gstr-9/table-8a': 'section-8a-details-api',
        'POST /gst/compliance/tax-payer/gstrs/gstr-9/save': 'save-gstr-9-api',
        'POST /gst/compliance/tax-payer/gstrs/gstr-9/file': 'file-gstr-9-api',
        
        # Status and Ledgers
        'GET /gst/compliance/tax-payer/gstrs/{year}/{month}/status': 'gstr-status-api',
        'GET /gst/compliance/tax-payer/invoices': 'get-invoices-api',
        'GET /gst/compliance/tax-payer/invoices/count': 'get-invoice-count-api',
        'GET /gst/compliance/tax-payer/invoices/status': 'check-invoice-status-api',
        'POST /gst/compliance/tax-payer/invoices/status/reset': 'reset-invoice-status-api',
        'POST /gst/compliance/tax-payer/invoices/status/save': 'save-invoice-status-api',
        'GET /gst/compliance/tax-payer/ledgers/cash': 'cash-ledger-api',
        'GET /gst/compliance/tax-payer/ledgers/itc': 'itc-ledger-api',
        'GET /gst/compliance/tax-payer/ledgers/tax/{year}/{month}': 'return-related-ledger-api',
        'GET /gst/compliance/tax-payer/ledgers/bal/{year}/{month}': 'cash-itc-balance-api',
        
        # E-Invoice APIs
        'POST /gst/compliance/e-invoice/tax-payer/authenticate': 'e-invoice-authentication-api',
        'POST /gst/compliance/e-invoice/tax-payer/invoice': 'generate-e-invoice-api',
        'GET /gst/compliance/e-invoice/tax-payer/invoice/{irn}': 'get-e-invoice-by-irn-api',
        'POST /gst/compliance/e-invoice/tax-payer/invoice/{irn}/cancel': 'cancel-e-invoice-api',
        'POST /gst/compliance/e-invoice/tax-payer/invoice/{irn}/e-way-bill': 'generate-e-way-bill-by-irn-api',
        'POST /gst/compliance/e-invoice/pdf/generate': 'generate-e-invoice-pdf-api',
        'GET /gst/compliance/e-invoice/tax-payer/gstin/search': 'irp-einv-search-gstin-details',
        'GET /gst/compliance/tax-payer/e-invoice/{irn}': 'taxpayer-get-e-invoice-by-irn-api',
        'POST /gst/compliance/tax-payer/e-invoices/{year}/{month}/sales': 'list-sales-e-invoices-job-api',
        'GET /gst/compliance/tax-payer/e-invoices/{year}/{month}/sales': 'list-sales-e-invoices-job-status-api',
        'POST /gst/compliance/tax-payer/e-invoices/{year}/{month}/purchases': 'list-purchase-e-invoices-job-api',
        'GET /gst/compliance/tax-payer/e-invoices/{year}/{month}/purchases': 'list-purchase-e-invoices-job-status-api',
        
        # E-Way Bill APIs
        'POST /gst/compliance/e-way-bill/tax-payer/authenticate': 'e-way-bill-authentication-api',
        'POST /gst/compliance/e-way-bill/consignor/bill': 'generate-e-way-bill-api',
        'POST /gst/compliance/e-way-bill/consignor/bill/{ewb_no}/cancel': 'cancel-e-way-bill-api',
        'POST /gst/compliance/e-way-bill/consignor/bill/{ewb_no}/extend': 'consigner-extend-e-way-bill-validity-api',
        'POST /gst/compliance/e-way-bill/consignor/bill/{ewb_no}/transporter': 'consigner-update-transporter-api',
        'POST /gst/compliance/e-way-bill/consignor/bill/{ewb_no}/vehicle': 'consignor-update-vehicle-details-api',
        'GET /gst/compliance/e-way-bill/consignor/bills': 'consignor-get-e-way-bills-by-date-api',
        'POST /gst/compliance/e-way-bill/consignee/bill/{ewb_no}/reject': 'reject-e-way-bill-api',
        'GET /gst/compliance/e-way-bill/consignee/bills': 'consignee-get-e-way-bills-by-date-api',
        'GET /gst/compliance/e-way-bill/tax-payer/bill/{ewb_no}': 'get-e-way-bill-api',
        'GET /gst/compliance/e-way-bill/tax-payer/error-list': 'get-error-list-api',
        'GET /gst/compliance/e-way-bill/tax-payer/gstin/search': 'e-way-bill-search-gstin-api',
        'GET /gst/compliance/e-way-bill/tax-payer/hsn': 'get-hsn-details-api',
        'GET /gst/compliance/e-way-bill/tax-payer/transin/search': 'search-transin-api',
        'POST /gst/compliance/e-way-bill/transporter/bill/{ewb_no}/extend': 'transporter-extend-e-way-bill-validity-api',
        'POST /gst/compliance/e-way-bill/transporter/bill/{ewb_no}/transporter': 'transporter-update-transporter-api',
        'POST /gst/compliance/e-way-bill/transporter/bill/{ewb_no}/vehicle': 'transporter-update-vehicle-details-part-b-api',
        'GET /gst/compliance/e-way-bill/transporter/bills': 'get-e-way-bills-by-date-and-state',
        'GET /gst/compliance/e-way-bill/transporter/bills/list': 'list-e-way-bills-by-generator',
    }
    
    # Add all direct mappings
    for api_key, slug in direct_mappings.items():
        if slug in gst_slugs:
            mapping[api_key] = slug
    
    # Save mapping
    with open('scripts/path_to_slug_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)
    
    print(f"\nCreated mapping for {len(mapping)} endpoints")
    print(f"All slugs verified against sitemap")
    
    # Show some examples
    print("\nSample mappings:")
    for i, (path, slug) in enumerate(list(mapping.items())[:5]):
        print(f"  {path} -> {slug}")
    
    return mapping

if __name__ == '__main__':
    create_mapping()

