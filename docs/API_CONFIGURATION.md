# API Configuration Guide

This guide provides detailed information on configuring API access for each service monitored by the Google Unified Dashboard.

## Overview

The dashboard collects data from four services:
1. **Gemini** - Google's AI model API
2. **Opal** - Identity and access management platform
3. **Wisk** - Cloud collaboration tool
4. **Polemi** - Data processing service

Each service requires API credentials and has specific configuration requirements.

## General Setup

All API credentials are configured through environment variables in the `.env` file:

```bash
cp .env.example .env
# Edit .env with your credentials
```

## 1. Gemini API Configuration

### Getting API Keys

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Select or create a Google Cloud project
4. Copy the API key

### Configuration

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_PROJECT_ID=your_gemini_project_id_here
```

### API Endpoints

The Gemini collector uses the following endpoints:
- Base URL: `https://generativelanguage.googleapis.com/v1`
- Models endpoint: `/models`
- Usage endpoint: Custom implementation based on your Gemini setup

### Required Permissions

- `generativelanguage.models.get`
- `generativelanguage.models.list`

### Notes

- API keys can be restricted by HTTP referrer, IP address, or application
- Monitor usage in Google Cloud Console
- Set up billing alerts to avoid unexpected charges

## 2. Opal API Configuration

### Getting API Keys

1. Log in to your Opal account
2. Navigate to Settings → API Keys
3. Click "Generate New API Key"
4. Copy and store the key securely

### Configuration

```env
OPAL_API_KEY=your_opal_api_key_here
OPAL_API_URL=https://api.opal.com
```

### API Endpoints

Default endpoints used:
- Base URL: `https://api.opal.com`
- Usage endpoint: `/usage`
- Analytics: `/analytics`

### Required Scopes

- `usage:read`
- `analytics:read`

### Rate Limits

- Standard tier: 100 requests/minute
- Enterprise tier: 1000 requests/minute

### Notes

- API keys should be kept confidential
- Rotate keys regularly for security
- Monitor usage in Opal dashboard

## 3. Wisk API Configuration

### Getting API Keys

1. Access your Wisk admin panel
2. Go to Integrations → API Access
3. Create a new API key
4. Set appropriate permissions

### Configuration

```env
WISK_API_KEY=your_wisk_api_key_here
WISK_API_URL=https://api.wisk.com
```

### API Endpoints

Default endpoints used:
- Base URL: `https://api.wisk.com`
- Usage endpoint: `/analytics/usage`
- Metrics: `/metrics`

### Required Permissions

- Read access to analytics
- Read access to usage metrics

### Authentication Method

Wisk uses API key authentication via header:
```
X-API-Key: your_api_key
```

### Rate Limits

- Free tier: 50 requests/hour
- Pro tier: 500 requests/hour
- Enterprise: Unlimited

### Notes

- API keys expire after 1 year
- Set calendar reminders for key rotation
- Test API access after configuration

## 4. Polemi API Configuration

### Getting API Keys

1. Log in to Polemi platform
2. Navigate to Account → Developer Settings
3. Generate API credentials
4. Note the API key and secret

### Configuration

```env
POLEMI_API_KEY=your_polemi_api_key_here
POLEMI_API_URL=https://api.polemi.com
```

### API Endpoints

Default endpoints used:
- Base URL: `https://api.polemi.com`
- Usage endpoint: `/v1/usage`
- Billing: `/v1/billing`

### Authentication Method

Bearer token authentication:
```
Authorization: Bearer your_api_key
```

### Required Scopes

- `usage.read`
- `billing.read`

### Rate Limits

- Standard: 200 requests/hour
- Premium: 1000 requests/hour

### Notes

- API keys can be scoped to specific resources
- Enable IP whitelisting for enhanced security
- Monitor API usage in Polemi dashboard

## Security Best Practices

### 1. Environment Variables

- Never commit `.env` file to version control
- Use `.env.example` as a template
- Store production credentials in secure secret management systems

### 2. API Key Rotation

Rotate API keys regularly:
- Gemini: Every 90 days
- Opal: Every 180 days
- Wisk: Annually
- Polemi: Every 90 days

### 3. Access Control

- Use service accounts where possible
- Apply principle of least privilege
- Audit API key usage regularly

### 4. Monitoring

- Set up alerts for unusual API activity
- Monitor rate limit consumption
- Track failed authentication attempts

## Testing API Configuration

Test your API configuration before running the full dashboard:

```javascript
// Create a simple test script
const axios = require('axios');

async function testGeminiAPI() {
  try {
    const response = await axios.get(
      'https://generativelanguage.googleapis.com/v1/models',
      {
        headers: {
          'Authorization': `Bearer ${process.env.GEMINI_API_KEY}`
        }
      }
    );
    console.log('✅ Gemini API: Connected');
  } catch (error) {
    console.error('❌ Gemini API: Failed -', error.message);
  }
}

// Run tests for all services
```

## Troubleshooting

### Authentication Errors

**Gemini**
- Error: "API key not valid"
- Solution: Regenerate API key in Google AI Studio

**Opal**
- Error: "Invalid credentials"
- Solution: Check API key hasn't expired

**Wisk**
- Error: "Unauthorized"
- Solution: Verify X-API-Key header format

**Polemi**
- Error: "Token expired"
- Solution: Generate new API token

### Rate Limiting

If you encounter rate limits:
1. Increase collection interval
2. Upgrade API tier if available
3. Implement exponential backoff
4. Contact support for rate limit increase

### Connection Issues

- Verify API URLs are correct
- Check firewall/proxy settings
- Test network connectivity to API endpoints
- Review service status pages

## Custom API Implementations

If your APIs use different endpoints or authentication methods, modify the collectors:

### Example: Custom Gemini Endpoint

Edit `src/collectors/gemini.js`:

```javascript
const response = await axios.get(
  `${customEndpoint}/your/custom/path`,
  {
    headers: {
      'Custom-Auth': `${this.apiKey}`
    }
  }
);
```

### Example: OAuth2 Authentication

For OAuth2-based APIs:

```javascript
// Add to collector
const oauth2Client = new OAuth2Client(
  clientId,
  clientSecret,
  redirectUri
);

// Get access token
const { tokens } = await oauth2Client.getToken(code);
oauth2Client.setCredentials(tokens);
```

## API Versioning

Track API versions to ensure compatibility:

- Gemini: v1
- Opal: v2.1
- Wisk: v1.3
- Polemi: v1.0

Update collectors when APIs are upgraded.

## Support and Resources

### Gemini
- [Google AI Documentation](https://ai.google.dev/docs)
- [API Reference](https://ai.google.dev/api)

### Opal
- Documentation: Contact Opal support
- Community: Opal user forums

### Wisk
- Documentation: Check Wisk developer portal
- Support: support@wisk.com

### Polemi
- Documentation: Polemi API docs
- Support: developer-support@polemi.com

## Next Steps

1. Configure at least one API service
2. Test API connectivity
3. Run initial data collection
4. Monitor logs for errors
5. Set up alerts for failures

For implementation help, see the main README or open a GitHub issue.
