import json
import xml.etree.ElementTree as ET
import re
from pathlib import Path

def parse_sitemap():
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

def create_path_to_slug_mapping():
    """Create a mapping from API paths to Readme slugs"""
    # Load OpenAPI spec
    with open('api-reference/gst/compliance/openapi.json', encoding='utf-8') as f:
        spec = json.load(f)
    
    paths = {p: spec['paths'][p] for p in spec['paths'].keys() if p.startswith('/gst/compliance/')}
    sitemap_slugs = parse_sitemap()
    
    # Create direct mapping
    mapping = {}
    
    # Direct mappings based on sitemap analysis
    path_to_slug = {
        '/gst/compliance/public/gstin/search': 'search-gstin-api',
        '/gst/compliance/public/pan/search': 'search-gstin-by-pan-api',
        '/gst/compliance/public/gstrs/track': 'track-gst-returns-api',
        '/gst/compliance/tax-payer/otp': 'taxpayer-generate-otp-api',
        '/gst/compliance/tax-payer/otp/verify': 'taxpayer-verify-otp-api',
        '/gst/compliance/tax-payer/session/refresh': 'taxpayer-refresh-access-token-api',
        '/gst/compliance/tax-payer/logout': 'taxpayer-logout-api',
        '/gst/compliance/tax-payer/evc/otp': 'generate-evc-otp-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/at/{year}/{month}': 'gstr-1-at-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/ata/{year}/{month}': 'gstr-1-ata-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/b2b/{year}/{month}': 'gstr-1-b2b-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/b2ba/{year}/{month}': 'gstr-1-b2ba-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/b2cl/{year}/{month}': 'gstr-1-b2cl-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/b2cla/{year}/{month}': 'gstr-1-b2cla-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/b2cs/{year}/{month}': 'gstr-1-b2cs-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/b2csa/{year}/{month}': 'gstr-1-b2csa-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/cdnr/{year}/{month}': 'gstr-1-cdnr-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/cdnra/{year}/{month}': 'gstr-1-cdnra-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/cdnur/{year}/{month}': 'gstr-1-cdnur-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/cdnura/{year}/{month}': 'gstr-1-cdnura-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/doc-issue/{year}/{month}': 'gstr-1-document-issued-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/exp/{year}/{month}': 'gstr-1-exp-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/expa/{year}/{month}': 'gstr-1-expa-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/nil/{year}/{month}': 'gstr-1-nil-supplies-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/hsn/{year}/{month}': 'gstr-1-hsn-summary-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/{year}/{month}': 'save-gstr-1-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/{year}/{month}/file': 'file-gstr-1-api',
        '/gst/compliance/tax-payer/gstrs/gstr-1/{year}/{month}/reset': 'reset-gstr-1-api',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/amdhist/{year}/{month}': 'gstr-2a-amdhist',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/b2b/{year}/{month}': 'gstr-2a-b2b-api',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/b2ba/{year}/{month}': 'gstr-2a-b2ba-api',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/cdn/{year}/{month}': 'gstr-2a-cdn-api',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/cdna/{year}/{month}': 'gstr-2a-cdna-api',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/impg/{year}/{month}': 'gstr-2a-impg',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/impgsez/{year}/{month}': 'gstr-2a-impgsez',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/isd/{year}/{month}': 'gstr-2a-isd-api',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/tcs/{year}/{month}': 'gstr-2a-tcs',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/tds/{year}/{month}': 'gstr-2a-tds',
        '/gst/compliance/tax-payer/gstrs/gstr-2a/{year}/{month}': 'gstr-2a-api',
        '/gst/compliance/tax-payer/gstrs/gstr-2b/{year}/{month}': 'gstr-2b-api',
        '/gst/compliance/tax-payer/gstrs/gstr-2b/regenerate': 'regenerate-gstr-2b',
        '/gst/compliance/tax-payer/gstrs/gstr-2b/{year}/{month}/regenerate': 'gstr-2b-regeneration-status',
        '/gst/compliance/tax-payer/gstrs/gstr-3b/{year}/{month}': 'gstr-3b-details-api',
        '/gst/compliance/tax-payer/gstrs/gstr-3b/{year}/{month}/file': 'file-gstr-3b-api',
        '/gst/compliance/tax-payer/gstrs/gstr-3b/{year}/{month}/offset-liability': 'gstr-3b-offset-liability',
        '/gst/compliance/tax-payer/gstrs/gstr-3b/{year}/{month}/auto-liability-calc': 'save-gstr-3b-api',
        '/gst/compliance/tax-payer/gstrs/gstr-3b/{year}/{month}/validate': 'save-gstr-3b-api',
        '/gst/compliance/tax-payer/gstrs/gstr-9': 'gstr-9-get-details-api',
        '/gst/compliance/tax-payer/gstrs/gstr-9/auto-calculated': 'gstr-9-auto-calculated-details-api',
        '/gst/compliance/tax-payer/gstrs/gstr-9/table-8a': 'section-8a-details-api',
        '/gst/compliance/tax-payer/gstrs/gstr-9/save': 'save-gstr-9-api',
        '/gst/compliance/tax-payer/gstrs/gstr-9/file': 'file-gstr-9-api',
        '/gst/compliance/tax-payer/gstrs/{year}/{month}/status': 'gstr-status-api',
        '/gst/compliance/tax-payer/gstrs/preference': 'remember-credentials-preference',
        '/gst/compliance/tax-payer/gstrs/{gstr}/{year}/{month}/proceed': 'proceed-to-file-api',
        '/gst/compliance/tax-payer/gstrs/{gstr}/{year}/{month}/new-proceed': 'new-proceed-to-file-api',
        '/gst/compliance/tax-payer/invoices': 'get-invoices-api',
        '/gst/compliance/tax-payer/invoices/count': 'get-invoice-count-api',
        '/gst/compliance/tax-payer/invoices/status': 'check-invoice-status-api',
        '/gst/compliance/tax-payer/invoices/status/reset': 'reset-invoice-status-api',
        '/gst/compliance/tax-payer/invoices/status/save': 'save-invoice-status-api',
        '/gst/compliance/tax-payer/ledgers/cash': 'cash-ledger-api',
        '/gst/compliance/tax-payer/ledgers/itc': 'itc-ledger-api',
        '/gst/compliance/tax-payer/ledgers/tax/{year}/{month}': 'return-related-ledger-api',
        '/gst/compliance/tax-payer/ledgers/bal/{year}/{month}': 'cash-itc-balance-api',
        '/gst/compliance/tax-payer/e-invoice/{irn}': 'taxpayer-get-e-invoice-by-irn-api',
        '/gst/compliance/tax-payer/e-invoices/{year}/{month}/sales': 'list-sales-e-invoices-job-api',
        '/gst/compliance/tax-payer/e-invoices/{year}/{month}/purchases': 'list-purchase-e-invoices-job-api',
        '/gst/compliance/e-invoice/tax-payer/authenticate': 'e-invoice-authentication-api',
        '/gst/compliance/e-invoice/tax-payer/invoice': 'generate-e-invoice-api',
        '/gst/compliance/e-invoice/tax-payer/invoice/{irn}': 'get-e-invoice-by-irn-api',
        '/gst/compliance/e-invoice/tax-payer/invoice/{irn}/cancel': 'cancel-e-invoice-api',
        '/gst/compliance/e-invoice/tax-payer/invoice/{irn}/e-way-bill': 'generate-e-way-bill-by-irn-api',
        '/gst/compliance/e-invoice/pdf/generate': 'generate-e-invoice-pdf-api',
        '/gst/compliance/e-invoice/tax-payer/gstin/search': 'irp-einv-search-gstin-details',
        '/gst/compliance/e-way-bill/tax-payer/authenticate': 'e-way-bill-authentication-api',
        '/gst/compliance/e-way-bill/consignor/bill': 'generate-e-way-bill-api',
        '/gst/compliance/e-way-bill/consignor/bill/{ewb_no}/cancel': 'cancel-e-way-bill-api',
        '/gst/compliance/e-way-bill/consignor/bill/{ewb_no}/extend': 'consigner-extend-e-way-bill-validity-api',
        '/gst/compliance/e-way-bill/consignor/bill/{ewb_no}/transporter': 'consigner-update-transporter-api',
        '/gst/compliance/e-way-bill/consignor/bill/{ewb_no}/vehicle': 'consignor-update-vehicle-details-api',
        '/gst/compliance/e-way-bill/consignor/bills': 'consignor-get-e-way-bills-by-date-api',
        '/gst/compliance/e-way-bill/consignee/bill/{ewb_no}/reject': 'reject-e-way-bill-api',
        '/gst/compliance/e-way-bill/consignee/bills': 'consignee-get-e-way-bills-by-date-api',
        '/gst/compliance/e-way-bill/tax-payer/bill/{ewb_no}': 'get-e-way-bill-api',
        '/gst/compliance/e-way-bill/tax-payer/error-list': 'get-error-list-api',
        '/gst/compliance/e-way-bill/tax-payer/gstin/search': 'e-way-bill-search-gstin-api',
        '/gst/compliance/e-way-bill/tax-payer/hsn': 'get-hsn-details-api',
        '/gst/compliance/e-way-bill/tax-payer/transin/search': 'search-transin-api',
        '/gst/compliance/e-way-bill/transporter/bill/{ewb_no}/extend': 'transporter-extend-e-way-bill-validity-api',
        '/gst/compliance/e-way-bill/transporter/bill/{ewb_no}/transporter': 'transporter-update-transporter-api',
        '/gst/compliance/e-way-bill/transporter/bill/{ewb_no}/vehicle': 'transporter-update-vehicle-details-part-b-api',
        '/gst/compliance/e-way-bill/transporter/bills': 'get-e-way-bills-by-date-and-state',
        '/gst/compliance/e-way-bill/transporter/bills/list': 'list-e-way-bills-by-generator',
    }
    
    # Save mapping to JSON for reference
    with open('scripts/path_to_slug_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(path_to_slug, f, indent=2)
    
    print(f"Created mapping for {len(path_to_slug)} paths")
    return path_to_slug

if __name__ == '__main__':
    create_path_to_slug_mapping()

