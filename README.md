# Google Unified Dashboard

Aggregates usage data from multiple Google and AI tools (Gemini, Opal, Wisk, Polemi) into Google Sheets, then visualizes it in Looker Studio for unified monitoring of costs, API usage, and resource consumption.

## Overview

This dashboard provides a centralized solution for:
- **Data Collection**: Automatically collects usage data from Gemini, Opal, Wisk, and Polemi APIs
- **Cost Calculation**: Calculates costs based on configurable pricing models
- **Data Aggregation**: Normalizes and aggregates data from multiple sources
- **Google Sheets Integration**: Stores all data in a structured Google Sheets spreadsheet
- **Looker Studio Visualization**: Easy connection to Looker Studio for real-time dashboards

## Features

- ✅ Multi-source data collection (Gemini, Opal, Wisk, Polemi)
- ✅ Automated cost calculation based on usage metrics
- ✅ Google Sheets integration for data storage
- ✅ Configurable collection intervals
- ✅ Standardized data format across all sources
- ✅ Ready for Looker Studio visualization
- ✅ Extensible architecture for adding new data sources

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Sources                             │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   Gemini     │    Opal      │    Wisk      │    Polemi      │
│   API        │    API       │    API       │    API         │
└──────┬───────┴──────┬───────┴──────┬───────┴──────┬─────────┘
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                      │
              ┌───────▼────────┐
              │  Data Collectors│
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │   Aggregator    │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │ Google Sheets   │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │ Looker Studio   │
              │   Dashboard     │
              └────────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Sheets API enabled
- Service Account credentials for Google Sheets
- API keys for Gemini, Opal, Wisk, and Polemi

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ArtradePro/google-unified-dashboard.git
   cd google-unified-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Sheets API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Sheets API and Google Drive API
   - Create a Service Account
   - Download the service account JSON key file
   - Save it as `service-account.json` in the project root

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   GOOGLE_SERVICE_ACCOUNT_PATH=service-account.json
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_PROJECT_ID=your_gemini_project_id
   OPAL_API_KEY=your_opal_api_key
   WISK_API_KEY=your_wisk_api_key
   POLEMI_API_KEY=your_polemi_api_key
   ```

5. **Configure settings (optional)**
   
   Edit `config.yaml` to customize:
   - Spreadsheet and worksheet names
   - Data collection intervals
   - Cost pricing models
   - Enable/disable specific data sources

## Usage

### Running the Dashboard

Run the data collection and aggregation:

```bash
python main.py
```

This will:
1. Collect usage data from all enabled sources
2. Aggregate and calculate costs
3. Write data to Google Sheets

### Scheduling Regular Updates

For regular data collection, use a scheduler like cron:

```bash
# Run every hour
0 * * * * cd /path/to/google-unified-dashboard && python main.py
```

Or use a cloud scheduler (e.g., Google Cloud Scheduler, AWS EventBridge).

## Looker Studio Integration

### Connecting to Google Sheets

1. Open [Looker Studio](https://lookerstudio.google.com/)
2. Create a new report
3. Click "Add Data"
4. Select "Google Sheets" as the connector
5. Choose the spreadsheet created by this dashboard
6. Select the "Aggregated Usage" worksheet

### Sample Visualizations

**Cost Overview Dashboard**
- Total cost by service (pie chart)
- Cost trends over time (time series)
- Top cost drivers (bar chart)

**Usage Metrics**
- API calls by service (bar chart)
- Token usage for Gemini (gauge)
- Active users and seats (scorecards)

**Resource Consumption**
- Storage usage (gauge)
- Compute hours (time series)
- Data transfers (area chart)

### Example Calculated Fields

In Looker Studio, you can create calculated fields for deeper insights:

```
Average Cost Per API Call = SUM(Calculated Cost USD) / SUM(API Calls)
Total Token Usage = Input Tokens + Output Tokens
Cost Per Token = Calculated Cost USD / (Input Tokens + Output Tokens)
```

## Configuration

### config.yaml

The main configuration file controls all aspects of the dashboard:

```yaml
google_sheets:
  spreadsheet_name: "Google Unified Dashboard - Usage Data"
  worksheet_name: "Aggregated Usage"
  credentials_path: "service-account.json"

sources:
  gemini:
    enabled: true
    api_key_env: "GEMINI_API_KEY"
  # ... other sources

aggregation:
  collection_interval: 60  # minutes
  historical_days: 30
  timezone: "UTC"

cost_mapping:
  gemini:
    input_token: 0.000001
    output_token: 0.000002
  # ... other cost mappings
```

### Cost Pricing

Update the `cost_mapping` section in `config.yaml` to match your actual pricing:

```yaml
cost_mapping:
  gemini:
    input_token: 0.000001   # Cost per input token
    output_token: 0.000002  # Cost per output token
  opal:
    api_call: 0.01          # Cost per API call
    user_seat: 50.00        # Monthly cost per user seat
  wisk:
    api_call: 0.005
    storage_gb: 0.10        # Cost per GB per month
  polemi:
    api_call: 0.008
    compute_hour: 0.50      # Cost per compute hour
```

## Project Structure

```
google-unified-dashboard/
├── main.py                          # Main application entry point
├── config.yaml                      # Configuration file
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── src/
│   ├── collectors/                  # Data collectors
│   │   ├── base_collector.py       # Base collector class
│   │   ├── gemini_collector.py     # Gemini data collector
│   │   ├── opal_collector.py       # Opal data collector
│   │   ├── wisk_collector.py       # Wisk data collector
│   │   └── polemi_collector.py     # Polemi data collector
│   ├── integrations/                # External integrations
│   │   └── sheets_integration.py   # Google Sheets integration
│   └── utils/                       # Utility modules
│       ├── aggregator.py            # Data aggregation logic
│       └── logger.py                # Logging configuration
└── tests/                           # Test files
```

## Data Schema

The aggregated data in Google Sheets follows this schema:

| Column | Description |
|--------|-------------|
| Timestamp | UTC timestamp of data collection |
| Service | Service name (gemini, opal, wisk, polemi) |
| Metric Type | Type of metric (api_usage, platform_usage, compute_usage) |
| Input Tokens | Number of input tokens (Gemini) |
| Output Tokens | Number of output tokens (Gemini) |
| API Calls | Number of API calls |
| Active Users | Number of active users |
| User Seats | Number of user seats |
| Storage GB | Storage used in GB |
| Compute Hours | Compute hours used |
| Data Transfers GB | Data transferred in GB |
| Resources Managed | Number of resources managed |
| Active Projects | Number of active projects |
| Active Jobs | Number of active jobs |
| Memory GB Hours | Memory GB hours used |
| Models | Models used (comma-separated) |
| Period Start | Start of measurement period |
| Period End | End of measurement period |
| Calculated Cost USD | Total calculated cost in USD |

## Extending the Dashboard

### Adding a New Data Source

1. Create a new collector in `src/collectors/`:
   ```python
   from src.collectors.base_collector import BaseCollector
   
   class NewServiceCollector(BaseCollector):
       def collect(self) -> List[Dict]:
           # Implement data collection logic
           pass
   ```

2. Add configuration in `config.yaml`:
   ```yaml
   sources:
     newservice:
       enabled: true
       api_key_env: "NEWSERVICE_API_KEY"
       endpoint: "https://api.newservice.com/v1"
   ```

3. Update `main.py` to include the new collector

4. Add cost mapping if needed

## Troubleshooting

### Common Issues

**Google Sheets Authentication Error**
- Verify the service account JSON file path
- Ensure the Google Sheets API is enabled in your project
- Check that the service account has necessary permissions

**No Data Collected**
- Verify API keys are correctly set in `.env`
- Check that services are enabled in `config.yaml`
- Review logs for specific error messages

**Cost Calculations Incorrect**
- Update cost mappings in `config.yaml` to match actual pricing
- Ensure metric names match between collectors and cost mapping

## Security Best Practices

- Never commit `.env` or `service-account.json` to version control
- Use environment-specific service accounts
- Rotate API keys regularly
- Restrict service account permissions to minimum required
- Use Secret Manager for production deployments

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Contact the maintainers

## Changelog

### Version 1.0.0 (2026-01-19)
- Initial release
- Support for Gemini, Opal, Wisk, and Polemi
- Google Sheets integration
- Automated cost calculation
- Looker Studio ready
