# Sandbox Documentation

This repository contains the documentation for Sandbox APIs, organized into the following sections:

## Documentation Structure

### 📚 Guides
Comprehensive guides covering:
- **Introduction**: About Sandbox and authentication
- **Get Started**: Basics, versioning, response caching, errors, rate limits, webhooks, and more
- **Products**: KYC, GST, TDS, and Income Tax product guides
- **Billing & Invoicing**: Subscription, quota, overdraft, wallet, and charges
- **Resources**: Postman collections, SDKs, and help center

### 🔌 API Reference
Complete API documentation organized by product:
- **Authentication**: API authentication endpoints
- **KYC**: Aadhaar, Bank, Digilocker, EntityLocker SDK, PAN verification APIs
- **GST**: Analytics and Compliance APIs (Public, Taxpayer, E-Invoice, E-Way Bill)
- **TDS**: Reports, Analytics, and Compliance APIs
- **Income Tax**: Tax calculation and compliance APIs
- **Bank**: Virtual Account APIs

### 🍳 Recipes
Step-by-step recipes and examples for:
- **KYC**: Digilocker API integration examples
- **GST**: GST workflow recipes
- **TDS**: TDS compliance recipes
- **IT**: Income Tax calculation recipes

### 📝 Changelog
Track all API updates, new features, improvements, and deprecations in the changelog.

### 📖 Knowledge Base
Access the knowledge base for additional resources and ecosystem information.

## Development

Install the [Mintlify CLI](https://www.npmjs.com/package/mint) to preview your documentation changes locally. To install, use the following command:

```
npm i -g mint
```

Run the following command at the root of your documentation, where your `docs.json` is located:

```
mint dev
```

View your local preview at `http://localhost:3000`.

## Publishing changes

Install our GitHub app from your [dashboard](https://dashboard.mintlify.com/settings/organization/github-app) to propagate changes from your repo to your deployment. Changes are deployed to production automatically after pushing to the default branch.

## Need help?

### Troubleshooting

- If your dev environment isn't running: Run `mint update` to ensure you have the most recent version of the CLI.
- If a page loads as a 404: Make sure you are running in a folder with a valid `docs.json`.

### Resources
- [Mintlify documentation](https://mintlify.com/docs)
