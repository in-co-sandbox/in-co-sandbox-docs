# KYC and KYB Context

## Overview

Know Your Customer (KYC) is a compliance process to verify customer identity before establishing a financial or business relationship. KYC verification prevents fraud, money laundering, and identity theft while ensuring regulatory compliance.

Know Your Business (KYB) is the business equivalent, verifying business identity, ownership, and compliance using government data.

Required across banking, fintech, insurance, lending, gaming, and any business handling payments or sensitive customer data.

## KYC - Know Your Customer

### Definition
Verify individual identity using trusted government data sources.

### Common Use Cases
1. **Customer onboarding**: Verify user identity during sign-up for financial services, fintech apps, and digital platforms
2. **Account opening**: Instant verification for bank accounts, wallets, and payment services
3. **Loan applications**: Validate borrower identity for personal loans, credit cards, and BNPL services
4. **Investment accounts**: KYC compliance for opening trading and demat accounts
5. **Gaming platforms**: Age and identity verification for online gaming and betting platforms
6. **Rental agreements**: Verify tenant identity for property rental and co-living spaces

### Verification Methods

#### Aadhaar Verification
- Most widely accepted proof of identity and address in India
- Issued by UIDAI (Unique Identification Authority of India)
- OTP-based verification flow
- Returns: Name, Date of Birth, Gender, Address, Photo

#### Digilocker
- Government platform for storing and sharing documents digitally
- Consent-based document retrieval following UIDAI and RBI guidelines
- Access government-issued documents: Aadhaar, PAN, Driving License, Vehicle Registration, Education Certificates, etc.
- Two integration options:
  - **Digilocker API**: Backend integration for full control over the flow
  - **Digilocker SDK**: Client-side SDK for iOS, Android, React Native, and Flutter
- Returns: Structured data in PDF, JPEG, or XML format
- User authenticates via Aadhaar OTP and grants consent to share specific documents
- Works with 250M+ registered Digilocker users
- Used for: Identity verification, address proof, KYC compliance, paperless verification

**Digilocker SDK Integration:**
- Pre-built UI for Digilocker authentication flow
- Three-step process: Create session → Initialize SDK → Handle response
- SDK manages complete flow including OTP verification and document selection
- Available platforms: Web (JavaScript), Android, iOS, Flutter
- Session-based architecture where backend creates session, client SDK uses it
- Customizable branding (logo, name) and theming (light/dark mode, colors)
- Event-driven callbacks for session completion, cancellation, or errors
- Use SDK for faster implementation; use API for full UI control

#### Bank Account Verification
- Verify bank account ownership for payments and payouts
- Methods: Penny Drop (small deposit verification), Penny Less (instant verification)
- Returns: Account holder name, account number, IFSC code
- Used for: Payment workflows, payout verification, UPI onboarding

#### PAN Verification (Individual)
- Permanent Account Number issued by Income Tax Department
- Verify PAN details and tax compliance
- Returns: Name, Date of Birth, PAN status
- Used for: Tax compliance, financial services onboarding

## KYB - Know Your Business

### Definition
Verify business identity, ownership, and compliance using government data. Critical for vendor onboarding, partner due diligence, B2B customer verification, and supply chain risk management.

### Common Use Cases
1. **Vendor onboarding**: Verify supplier legitimacy before establishing business relationships
2. **Partner verification**: Validate distributors, resellers, and business partners
3. **Credit assessment**: Check business credentials before extending credit or payment terms
4. **Compliance checks**: Ensure vendors and partners meet regulatory requirements
5. **Marketplace verification**: Screen sellers and service providers on B2B platforms

Streamline business verification to reduce onboarding time from days to minutes while mitigating fraud and compliance risks.

### Verification Methods

#### CIN & DIN Verification
- Corporate Identity Number (CIN) and Director Identification Number (DIN)
- Ministry of Corporate Affairs (MCA) data
- Verify company registration, directors, corporate structure
- Returns: Company details, director information, registration status
- Governed by: Companies Act, 2013

#### GSTIN Verification
- Goods and Services Tax Identification Number
- Verify business GST registration, filing status, operational details
- Returns: Business name, address, registration status, filing history
- Used for: Tax compliance verification, business legitimacy checks

#### PAN Verification (Business)
- Verify business PAN for financial activity and regulatory compliance
- Returns: Business name, PAN status, constitution type
- Used for: Risk assessment, partner due diligence

#### Udyam Certificate
- Ministry of MSME (Micro, Small and Medium Enterprises)
- Verify MSME registration and status
- Returns: Business identity, MSME classification, PAN and GSTIN linkage
- Used for: MSME verification, government tender participation

#### EntityLocker
- Government platform for storing and sharing business documents digitally (Digilocker for businesses)
- Consent-based retrieval of business credentials
- Access verified business documents: GSTIN details, Company Master Data from MCA, Udyam certificates, Certificate of Incorporation, Business PAN
- Two integration options:
  - **EntityLocker API**: Backend integration for custom B2B workflows
  - **EntityLocker SDK**: Client-side SDK for web and mobile applications
- Returns: Business documents in PDF or JSON format
- Authorized representatives authenticate and grant consent to share documents
- Retrieved documents retained for 60 minutes before automatic deletion
- Used for: Vendor onboarding, KYB compliance, partner verification, business credential validation, B2B account opening

## API Patterns

### Authentication
All KYC/KYB APIs use the same authentication pattern:
- Bearer token authentication
- API key format: `key_test_...` (test environment) or `key_live_...` (production)

### Response Structure
Consistent response formats across all verification methods:
- Success responses include verification status and data
- Error responses follow standard error format
- All timestamps in ISO 8601 format

### Verification Flow
1. Initiate verification request
2. For OTP-based methods: Generate OTP → Verify OTP
3. For instant methods: Single API call returns verification result
4. For consent-based methods: Initiate session → Check status → Fetch documents

## Terminology

- **KYC**: Know Your Customer - individual identity verification
- **KYB**: Know Your Business - business identity verification
- **Aadhaar**: 12-digit unique identity number for Indian residents
- **PAN**: Permanent Account Number - 10-character alphanumeric tax ID
- **GSTIN**: 15-digit GST Identification Number
- **CIN**: 21-character Corporate Identity Number
- **DIN**: 8-digit Director Identification Number
- **Udyam**: MSME registration certificate
- **Digilocker**: Digital locker for storing government-issued documents
- **EntityLocker**: Digital locker for business documents
- *Documentation Writing Guidelines

When writing KYC/KYB overview pages:
- Use documentation tone, not marketing language
- Focus on helping users identify if the solution fits their use case
- Avoid promotional phrases like "instantly", "streamline", "seamless", "frictionless"
- Use factual descriptions: "Use this API to..." instead of "Get access to..."
- Lead with what the service is, then explain capabilities
- Keep content concise - remove unnecessary words
- Use "How it works" for process flows, "What you can do" for capabilities
- List use cases as specific technical requirements, not industry buzzwords
- Integration options should explain the differences clearly
- FAQs should be direct and technical, not persuasive

## Keywords for SEO
- KYC, KYC API, Know Your Customer
- KYB, Know Your Business
- identity verification, kyc verification api
- Aadhaar verification, Aadhaar API
- PAN verification, PAN API
- GSTIN verification, GST verification
- Digilocker, Digilocker API, Digilocker SDK
- EntityLocker, EntityLocker API, EntityLocker SDK
- bank verification, bank account verification
- MCA verification, company verification
- vendor onboarding, partner verification
- consent-based verification, document retrieval
- PAN verification, PAN API
- GSTIN verification, GST verification
- Digilocker, Digilocker API
- bank verification, bank account verification
- MCA verification, company verification
- vendor onboarding, partner verification
