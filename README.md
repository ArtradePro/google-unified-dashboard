# Google Unified Dashboard

A comprehensive solution for aggregating usage data from multiple Google and AI tools (Gemini, Opal, Wisk, Polemi) into Google Sheets, then visualizing it in Looker Studio for unified monitoring of costs, API usage, and resource consumption.

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 15 minutes
- **[API Configuration](docs/API_CONFIGURATION.md)** - Configure service API keys
- **[Looker Studio Setup](docs/LOOKER_STUDIO_SETUP.md)** - Create visualizations
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment options
- **[Contributing](CONTRIBUTING.md)** - How to contribute
- **[Changelog](CHANGELOG.md)** - Version history

## Overview

This dashboard provides:
- **Automated Data Collection**: Collects usage metrics from Gemini, Opal, Wisk, and Polemi APIs
- **Centralized Storage**: Aggregates all data into Google Sheets for easy access
- **Unified Monitoring**: Track costs, API calls, and resource consumption across all platforms
- **Looker Studio Integration**: Visualize trends and insights through interactive dashboards

## Features

- ✅ Multi-service data aggregation (Gemini, Opal, Wisk, Polemi)
- ✅ Automated data collection with configurable intervals
- ✅ Google Sheets integration for data storage
- ✅ Comprehensive logging and error handling
- ✅ Summary statistics and metrics
- ✅ Looker Studio ready data format

## Prerequisites

- Node.js 14.x or higher
- npm or yarn
- Google Cloud Project with Sheets API enabled
- API keys for services you want to monitor (Gemini, Opal, Wisk, Polemi)
- Google Sheets spreadsheet for data storage

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ArtradePro/google-unified-dashboard.git
cd google-unified-dashboard
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Set up Google Sheets API credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Sheets API
   - Create a service account
   - Download credentials as JSON
   - Save as `credentials.json` in the project root

## Configuration

### Environment Variables

Edit the `.env` file with your configuration:

```env
# Required: Google Sheets Configuration
GOOGLE_SHEET_ID=your_spreadsheet_id
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

# Optional: API Keys (configure only services you want to monitor)
GEMINI_API_KEY=your_gemini_api_key
GEMINI_PROJECT_ID=your_project_id

OPAL_API_KEY=your_opal_api_key
OPAL_API_URL=https://api.opal.com

WISK_API_KEY=your_wisk_api_key
WISK_API_URL=https://api.wisk.com

POLEMI_API_KEY=your_polemi_api_key
POLEMI_API_URL=https://api.polemi.com

# Collection Interval (0 for single run, >0 for continuous)
COLLECTION_INTERVAL_MINUTES=60

# Logging Level
LOG_LEVEL=info
```

### Google Sheets Setup

1. Create a new Google Sheets spreadsheet
2. Note the spreadsheet ID from the URL: 
   `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
3. Share the spreadsheet with the service account email (found in credentials.json)
4. The application will automatically create two sheets:
   - `UsageData`: Raw usage data from all services
   - `Summary`: Aggregated metrics and statistics

## Usage

### Single Execution

Run once and collect current data:
```bash
npm start
```

or set `COLLECTION_INTERVAL_MINUTES=0` in `.env`

### Continuous Monitoring

Run continuously with scheduled collection:
```bash
# Set COLLECTION_INTERVAL_MINUTES=60 (or desired interval)
npm start
```

The application will collect data at the specified interval until stopped (Ctrl+C).

### Running as a Service

For production deployment, use a process manager like PM2:

```bash
# Install PM2
npm install -g pm2

# Start the application
pm2 start src/index.js --name google-dashboard

# Configure to start on boot
pm2 startup
pm2 save
```

## Looker Studio Integration

### Connecting to Google Sheets

1. Open [Looker Studio](https://lookerstudio.google.com/)
2. Click "Create" → "Data Source"
3. Select "Google Sheets"
4. Choose your spreadsheet and select the `UsageData` sheet
5. Click "Connect"

### Creating Your Dashboard

1. Create a new report
2. Add your Google Sheets data source
3. Recommended visualizations:
   - **Time Series Chart**: Track costs over time
   - **Scorecard**: Display total API calls and costs
   - **Table**: Show detailed usage by service
   - **Pie Chart**: Compare costs across services
   - **Bar Chart**: API calls per service

### Sample Metrics

- Total Costs (Sum of Costs field)
- Total API Calls (Sum of API Calls field)
- Cost per Service (Group by Service)
- Trends over Time (Date range with Timestamp)
- Error Rate (Count of records with Status = 'error')

## Data Schema

### UsageData Sheet

| Column | Description |
|--------|-------------|
| Timestamp | ISO 8601 timestamp of data collection |
| Service | Service name (Gemini, Opal, Wisk, Polemi) |
| API Calls | Number of API calls made |
| Costs ($) | Total costs in USD |
| Status | Collection status (success/error) |
| Additional Metrics | JSON object with service-specific metrics |
| Error | Error message if collection failed |

### Summary Sheet

| Metric | Description |
|--------|-------------|
| Total API Calls | Sum of all API calls across services |
| Total Costs ($) | Sum of all costs across services |
| Last Updated | Timestamp of last data collection |
| Services Monitored | Number of active services |

## Architecture

```
┌─────────────────────────────────────────────┐
│           Data Collection Layer              │
├─────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │  Gemini  │ │   Opal   │ │   Wisk   │   │
│  │Collector │ │Collector │ │Collector │   │
│  └──────────┘ └──────────┘ └──────────┘   │
│       │            │            │           │
│       └────────────┴────────────┴───────┐   │
│                                         │   │
│  ┌──────────┐                          │   │
│  │  Polemi  │                          │   │
│  │Collector │                          │   │
│  └──────────┘                          │   │
│       │                                │   │
│       └────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│         Aggregation Service                  │
│  • Collects data from all sources           │
│  • Calculates summary statistics            │
│  • Handles errors gracefully                │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│      Google Sheets Service                   │
│  • Writes data to spreadsheet               │
│  • Updates summary sheet                    │
│  • Manages sheet structure                  │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│          Google Sheets                       │
│  • UsageData sheet (raw data)               │
│  • Summary sheet (aggregated metrics)       │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│         Looker Studio Dashboard              │
│  • Real-time visualizations                 │
│  • Cost tracking and trends                 │
│  • Resource consumption metrics             │
└─────────────────────────────────────────────┘
```

## Troubleshooting

### Authentication Errors

**Problem**: "Failed to initialize Google Sheets API"

**Solution**: 
- Verify `credentials.json` exists and is valid
- Ensure the service account has access to the spreadsheet
- Check that Sheets API is enabled in Google Cloud Console

### API Collection Failures

**Problem**: "Error collecting [Service] data"

**Solutions**:
- Verify API keys are correct in `.env`
- Check API endpoints are accessible
- Review service-specific API documentation
- Check logs in `logs/error.log` for details

### Missing Data

**Problem**: No data appearing in Google Sheets

**Solutions**:
- Check `GOOGLE_SHEET_ID` is correct
- Verify service account has "Editor" access
- Check logs for errors
- Ensure at least one API key is configured

## Logging

Logs are written to:
- `logs/combined.log` - All log messages
- `logs/error.log` - Error messages only
- Console - Formatted output with colors

Adjust log level with `LOG_LEVEL` environment variable (error, warn, info, debug).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
