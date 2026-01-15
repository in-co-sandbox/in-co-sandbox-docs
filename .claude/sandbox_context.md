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

## Important notes

- Never mix test and production credentials
- Test environment mirrors production functionality
- API calls in test environment are free
- API calls in production environment are billed
