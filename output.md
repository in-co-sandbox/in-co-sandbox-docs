
| Param | Type | Description |
| --- | --- | --- |
| challan_serial | string | Bank Challan No |
| bsr_code | string | Bank-Branch Code/ Form 24G Receipt Number |
| paid_date_epoch | number | EPOCH timestamp of the challan paid date |
| minor_head | enumeration | Minor Head of challan |
| tds_amount | number | Income Tax |
| surcharge | number | Surcharge on Income Tax |
| health_and_education_cess | number | Education cess on Income Tax |
| interest | number | Interest levied upon late deduction |
| late_filing_fees | number | Penalty levied upon late filing |
| other_penalty | number | Any Other Penalty |
| utilized_amount | number | Total Amount of Challan Utilised  <br />in previous returns.  |
| notice | string | Type of notice applicable from this challan. Possible values: short_payment, late_payment, short_&\_late_payment |
| notice_reason | string | Reason for the applicable notice |
| challan_available | number | Challan amount available for this return after deducting the utilized amount. |
| utilized_amount_in_payments | number | Challan amount utilized in the payment_sheet |
| short_payment | number | The amount that exceeds the available challan for this return. |
| challan_due_date | number | The date at which the challan should be deposited.  |
| interest_payable | number | Penalty interest payable due to the notice |
| additional_tds_to_be_deposited | number | Additional amount to be paid, which is the sum of the short_payment and interest_payable. |

