# Looker Studio Setup Guide

This guide walks you through setting up your Looker Studio dashboard to visualize data from the Google Unified Dashboard.

## Prerequisites

- Completed setup of the Google Unified Dashboard
- Data collected and stored in Google Sheets
- Access to Looker Studio (free with Google account)

## Step 1: Create Data Source

1. Navigate to [Looker Studio](https://lookerstudio.google.com/)
2. Click **Create** → **Data Source**
3. Search for and select **Google Sheets** connector
4. Choose your Google account
5. Select the spreadsheet containing your usage data
6. Select the **UsageData** worksheet
7. Click **Connect** in the top-right corner

## Step 2: Configure Data Types

Review and adjust field types if needed:

| Field Name | Type | Aggregation |
|------------|------|-------------|
| Timestamp | Date & Time | None |
| Service | Text | None |
| API Calls | Number | Sum |
| Costs ($) | Number | Sum |
| Status | Text | None |
| Additional Metrics | Text | None |
| Error | Text | None |

Click **Create Report** when ready.

## Step 3: Create Dashboard Layout

### Recommended Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    Dashboard Header                         │
│  Google Unified Dashboard - Usage & Cost Monitoring         │
└─────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Total Costs  │  API Calls   │   Services   │  Last Update │
│   $XXX.XX    │   XX,XXX     │      4       │  XX:XX AM    │
└──────────────┴──────────────┴──────────────┴──────────────┘

┌─────────────────────────────────────────────────────────────┐
│          Cost Trend Over Time (Time Series)                 │
│                                                             │
│  [Line chart showing costs by service over time]           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌────────────────────────┬─────────────────────────────────────┐
│  Cost by Service       │   API Calls by Service              │
│  (Pie Chart)          │   (Bar Chart)                       │
│                        │                                     │
│  [Pie chart]          │   [Bar chart]                       │
│                        │                                     │
└────────────────────────┴─────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Detailed Usage Table                           │
│                                                             │
│  [Scrollable table with all data]                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Step 4: Add Visualizations

### 1. Total Costs Scorecard

1. Click **Add a chart** → **Scorecard**
2. Drag to desired position
3. In the properties panel:
   - Metric: Select **Costs ($)**
   - Aggregation: **Sum**
   - Optional: Add comparison to previous period

### 2. Total API Calls Scorecard

1. Add another **Scorecard**
2. Configure:
   - Metric: **API Calls**
   - Aggregation: **Sum**

### 3. Services Count Scorecard

1. Add another **Scorecard**
2. Configure:
   - Metric: **Service**
   - Aggregation: **Count Distinct**

### 4. Last Update Scorecard

1. Add another **Scorecard**
2. Configure:
   - Metric: **Timestamp**
   - Aggregation: **Max**

### 5. Cost Trend Time Series

1. Click **Add a chart** → **Time series chart**
2. Configure:
   - Dimension: **Timestamp** (Date Hour or Date)
   - Breakdown Dimension: **Service**
   - Metric: **Costs ($)** - Sum
   - Optional: Add smoothing for better visualization

### 6. Cost by Service Pie Chart

1. Click **Add a chart** → **Pie chart**
2. Configure:
   - Dimension: **Service**
   - Metric: **Costs ($)** - Sum
   - Sort: By metric (descending)

### 7. API Calls Bar Chart

1. Click **Add a chart** → **Bar chart**
2. Configure:
   - Dimension: **Service**
   - Metric: **API Calls** - Sum
   - Sort: By metric (descending)

### 8. Detailed Usage Table

1. Click **Add a chart** → **Table**
2. Configure:
   - Dimensions: **Timestamp**, **Service**, **Status**
   - Metrics: **API Calls** (Sum), **Costs ($)** (Sum)
   - Sort: By timestamp (descending)
   - Rows per page: 10-20

## Step 5: Add Filters

### Date Range Filter

1. Click **Add a control** → **Date range control**
2. Place at the top of the dashboard
3. Configure:
   - Default date range: Last 30 days
   - Auto update: Yes

### Service Filter

1. Click **Add a control** → **Drop-down list**
2. Configure:
   - Control field: **Service**
   - Allow multiple selections: Yes
   - Include "All" option: Yes

### Status Filter

1. Add another **Drop-down list**
2. Configure:
   - Control field: **Status**
   - Include options: Success, Error

## Step 6: Styling and Formatting

### Color Scheme

Use consistent colors for services:
- **Gemini**: Blue (#4285F4)
- **Opal**: Purple (#9334E6)
- **Wisk**: Green (#34A853)
- **Polemi**: Red (#EA4335)

### Apply Theme

1. Click **Theme and layout** (top menu)
2. Choose a theme or customize:
   - Background: White or Light gray
   - Chart colors: Use service color scheme
   - Font: Roboto or Google Sans

## Step 7: Add Calculated Fields (Optional)

### Cost per API Call

1. Click **Add a field** (in data source editor)
2. Name: `Cost per API Call`
3. Formula: `SUM(Costs ($)) / SUM(API Calls)`

### Error Rate

1. Add field: `Error Rate`
2. Formula: 
```
CASE 
  WHEN Status = "error" THEN 1
  ELSE 0
END
```

## Step 8: Configure Alerts (Optional)

Set up email alerts for:
- Costs exceeding threshold
- High error rates
- Unusual API usage patterns

## Best Practices

1. **Refresh Schedule**: Enable automatic data refresh (every hour)
2. **Mobile Optimization**: Test dashboard on mobile devices
3. **Performance**: Limit date ranges for better performance
4. **Sharing**: Share with appropriate team members
5. **Versioning**: Save versions before major changes

## Sample Dashboard Templates

### Executive Summary Dashboard

Focus on:
- High-level cost metrics
- Trend analysis
- Service comparison

### Technical Operations Dashboard

Focus on:
- Detailed API metrics
- Error tracking
- Resource utilization

### Cost Optimization Dashboard

Focus on:
- Cost breakdown by service
- Usage efficiency metrics
- Anomaly detection

## Troubleshooting

### Data Not Updating

- Check Google Sheets has new data
- Refresh the data source manually
- Verify data source connection

### Missing Services

- Ensure all services have API keys configured
- Check collection logs for errors
- Verify data in Google Sheets

### Incorrect Aggregations

- Review field types in data source
- Check aggregation settings on each chart
- Verify date range filters

## Advanced Features

### Blending Data Sources

Combine with other data sources:
1. Click **Resource** → **Manage added data sources**
2. Add additional sources
3. Create data blends for cross-analysis

### Custom Queries

Use Google Sheets formulas for:
- Advanced calculations
- Data transformations
- Custom aggregations

## Resources

- [Looker Studio Help Center](https://support.google.com/looker-studio)
- [Community Gallery](https://lookerstudio.google.com/gallery) - Template examples
- [Data Studio Community](https://www.en.advertisercommunity.com/t5/Data-Studio/ct-p/data-studio) - Get help

## Next Steps

1. Customize dashboard to your needs
2. Share with team members
3. Set up scheduled email reports
4. Monitor and optimize based on insights

For issues or questions, refer to the main README or open a GitHub issue.
