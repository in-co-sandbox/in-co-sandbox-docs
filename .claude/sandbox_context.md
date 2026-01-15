# Sandbox API context

This file contains important contextual information about the Sandbox API platform to help maintain consistency across documentation.

## Environments

Sandbox provides two separate environments:

### Test environment
- **Host URL**: `https://test-api.sandbox.co.in`
- **Purpose**: Development and testing without charges
- **Credentials prefix**: `key_test`
- **Billing**: Free

### Production environment
- **Host URL**: `https://api.sandbox.co.in`
- **Purpose**: Live integrations with real data
- **Credentials prefix**: `key_live`
- **Billing**: Billed according to subscription plan

## API credentials structure

### API key format
- Test: `key_test...` (followed by additional characters)
- Live: `key_live...` (followed by additional characters)

### API secret
- Shown only once when generated
- Must be saved immediately upon creation
- Cannot be retrieved again after initial display

### Authentication
- Access tokens are generated using the Authenticate API
- Access tokens are valid for 24 hours
- Access tokens are NOT bearer tokens (don't use "Bearer" prefix in authorization header)

## Required headers for API calls

All API requests require:
- `x-api-key`: Your API Key
- `authorization`: Your access token (without "Bearer" prefix)
- `x-api-version`: API version (e.g., "1.0") - optional

## Request & response structure

### Request methods
- GET: Retrieve data (path/query parameters)
- POST: Create/submit data (JSON body)
- PUT: Update data (JSON body)
- DELETE: Remove data (path/query parameters)

### Standard response format
```json
{
  "code": 200,
  "data": { /* response data */ },
  "timestamp": 1750687659809,
  "transaction_id": "unique-id"
}
```

### Common headers
- `x-api-key` (required): API key (e.g., key_live_SIethxxxxxxxx)
- `authorization` (required): JWT access token (no "Bearer" prefix)
- `x-api-secret`: API secret (only for Authenticate API)
- `x-api-version`: API version (e.g., "1.0") - optional
- `x-source`: Data source (default: primary) - optional
- `Cache-Control`: Set to "no-cache" for latest data - optional
- `Content-Type`: Usually "application/json" - optional

### Special formats
- Some APIs use sheet structure format for bulk operations

## Versioning

### Semantic versioning format
- Format: `MAJOR.MINOR.PATCH`
- Major: Backward-incompatible changes (e.g., 1.0.0 → 2.0.0)
- Minor: New features, backward compatible (e.g., 2.0.0 → 2.1.0)
- Patch: Bug fixes, backward compatible (e.g., 2.1.0 → 2.1.1)

### Version specification
- Optional header: `x-api-version` (e.g., "1.0")
- Without version header: Uses latest stable version
- Sandbox APIs always use latest version
- Version header only affects response format for specific endpoints

### Version lifecycle
- **Deprecation**: Older versions no longer maintained but still functional
- **Discontinuation**: Deprecated versions eventually stopped, returns 503 errors
- Communicated via: Changelog, email notifications, API reference pages

## Important notes

- Never mix test and production credentials
- Test environment mirrors production functionality
- API calls in test environment are free
- API calls in production environment are billed
