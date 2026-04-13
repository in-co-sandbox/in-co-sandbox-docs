# Taxpayer API schema status

Generated on: 2026-04-13

Scope: `api-reference/gst/compliance/endpoints/taxpayer/**/*.mdx`

Status rule:
- `POST` and `PUT` endpoints are `Present` only if the page contains a request body schema card inside a `CardGroup`.
- `GET` endpoints are `Present` only if the page contains a response body schema card inside a `CardGroup`.

## Summary

| Metric | Count |
| --- | ---: |
| Total endpoint pages scanned | 78 |
| Present | 68 |
| Missing | 1 |

## API status

| Method | File | Expected schema | Status |
| --- | --- | --- | --- |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/common/get_filing_preference.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/common/gst_return_status.mdx` | Response body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/common/save_filing_preference.mdx` | Request body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/e-invoice/e_invoice.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/at.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/ata.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/b2b.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/b2ba.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/b2cl.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/b2cla.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/b2cs.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/b2csa.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/cdnr.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/cdnra.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/cdnur.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/cdnura.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/doc_issue.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/ecom.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/ecoma.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/exp.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/expa.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/get_hsn.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/nil.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/supeco.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/supecoa.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/txp.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/txpa.mdx` | Response body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/file/file.mdx` | Request body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/file/new_proceed.mdx` | Request body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/file/reset.mdx` | Request body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-1/file/save.mdx` | Request body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/amdhist.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/b2b.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/b2ba.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/cdn.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/cdna.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/document.mdx` | Response body schema | Missing |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/ecom.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/ecoma.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/impg.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/impgsez.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/isd.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/tcs.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2a/tds.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2b/document.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2b/gstr_2b_regeneration_status.mdx` | Response body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-2b/regenerate_gstr_2b.mdx` | Request body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-3b/auto_liability_calc.mdx` | Response body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-3b/file.mdx` | Request body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-3b/gstr_3b_details.mdx` | Response body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-3b/offset_liability.mdx` | Request body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-3b/save.mdx` | Request body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-9/auto_calculated_details.mdx` | Response body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-9/file.mdx` | Request body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-9/gstr_9_details.mdx` | Response body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-9/proceed.mdx` | Request body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/gstr-9/save.mdx` | Request body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/gstr-9/section_8a_details.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/invoices/added-back-liabilities.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/invoices/invoice_count.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/invoices/invoices.mdx` | Response body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/invoices/reset.mdx` | Request body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/invoices/sales.mdx` | Response body schema | Present |
| POST | `api-reference/gst/compliance/endpoints/taxpayer/invoices/save.mdx` | Request body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/invoices/status.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/ledgers/cash_itc_balance_ledger.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/ledgers/cash_ledger.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/ledgers/itc_ledger.mdx` | Response body schema | Present |
| GET | `api-reference/gst/compliance/endpoints/taxpayer/ledgers/return_liability_ledger.mdx` | Response body schema | Present |


