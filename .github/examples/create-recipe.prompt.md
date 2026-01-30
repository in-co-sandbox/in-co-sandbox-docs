**Title**: File GSTR-9
**Description**: GSTR-9 is an annual GST return summarizing a taxpayer's filings, including supplies, taxes paid, ITC, and adjustments or refunds for the financial year. This recipe takes you through the steps to file GSTR-9.

**API Steps**:
1. Get Taxpayer Session
This recipe takes you through the steps to get a GST Taxpayer access token.
Link: https://developer.sandbox.co.in/recipes/gst/authentication/generate_tax_payer_session

2. Get GSTR-9 Auto Calculated Details
Fetch the auto-calculated table details in the GSTR-9 as available with the GST Department.
Link: https://developer.sandbox.co.in/api-reference/gst/compliance/endpoints/taxpayer/gstr-9/auto_calculated_details

3. GSTR-1 HSN Summary
Get HSN summary for outward supplies in specified return period for authenticated taxpayer. Pull this for the year to populate the Table 17 in GSTR-9.
Link: https://developer.sandbox.co.in/api-reference/gst/compliance/endpoints/taxpayer/gstr-1/documents/get_hsn
4. Save GSTR-9
Save the GSTR-9 with the required data across tables including outward supplies, input tax credits (ITC), and tax payments for the financial year with the GST department.
link: https://developer.sandbox.co.in/api-reference/gst/compliance/endpoints/taxpayer/gstr-9/save
5. GST Return Status
Check the status of the return after previous action.

Link: https://developer.sandbox.co.in/api-reference/gst/compliance/endpoints/taxpayer/common/gst_return_status

6. Get GSTR-9 Details
Fetch GSTR-9 details saved with the Save GSTR-9 API. This data needs to be passed in the File GSTR-9 API to complete the filing workflow.
Link: https://developer.sandbox.co.in/reference/gstr-9-get-details-api

7. Proceed to file
Proceed to file marks the return ready for filing. Post this EVC OTP can be generated for filing.
link: https://developer.sandbox.co.in/api-reference/gst/compliance/endpoints/taxpayer/gstr-9/proceed
8. GST Return Status
Check the status of the return after previous action.
https://developer.sandbox.co.in/api-reference/gst/compliance/endpoints/taxpayer/common/gst_return_status
9. Generate EVC OTP
Generate the EVC OTP required to file a GST Return.
https://developer.sandbox.co.in/api-reference/gst/compliance/endpoints/taxpayer/authentication/generate_evc_otp
10. File GSTR-9
File the GSTR-9 Return by passing the financial year, PAN, EVC OTP and GSTR-9 Details in the request.
Link: https://developer.sandbox.co.in/api-reference/gst/compliance/endpoints/taxpayer/gstr-9/file
