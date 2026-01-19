# Looker Studio Setup Guide

This guide explains how to connect your Google Sheets data to Looker Studio and create visualizations.

## Prerequisites

- Access to the Google Sheets spreadsheet created by the dashboard
- Google account with Looker Studio access

## Step-by-Step Setup

### 1. Access Looker Studio

1. Go to [https://lookerstudio.google.com/](https://lookerstudio.google.com/)
2. Sign in with your Google account

### 2. Create a New Report

1. Click on the **"+"** button or **"Create"** → **"Report"**
2. You'll be prompted to add a data source

### 3. Connect Google Sheets

1. In the "Add data to report" panel, search for **"Google Sheets"**
2. Click on the **Google Sheets** connector
3. Select the **"Google Unified Dashboard - Usage Data"** spreadsheet
4. Choose the **"Aggregated Usage"** worksheet
5. Click **"Add"** and then **"Add to Report"**

### 4. Configure Data Types (Optional but Recommended)

1. Click on **"Resource"** → **"Manage added data sources"**
2. Click on your data source
3. Verify field types:
   - Timestamp: Date & Time
   - Calculated Cost USD: Currency (USD)
   - All numeric fields: Number
   - All text fields: Text

### 5. Create Your First Visualization

#### Cost Overview Chart

1. Click **"Add a chart"** → **"Pie chart"**
2. Configure:
   - **Dimension**: Service
   - **Metric**: SUM of Calculated Cost USD
3. Style the chart with appropriate colors

#### Cost Trend Time Series

1. Click **"Add a chart"** → **"Time series chart"**
2. Configure:
   - **Date Range Dimension**: Timestamp
   - **Dimension**: Service
   - **Metric**: SUM of Calculated Cost USD
3. Adjust time granularity as needed (Day/Week/Month)

#### API Usage Bar Chart

1. Click **"Add a chart"** → **"Bar chart"**
2. Configure:
   - **Dimension**: Service
   - **Metric**: SUM of API Calls
3. Sort by metric descending

### 6. Add Scorecards for Key Metrics

Create scorecards for:
- **Total Cost**: SUM(Calculated Cost USD)
- **Total API Calls**: SUM(API Calls)
- **Total Storage GB**: SUM(Storage GB)
- **Total Compute Hours**: SUM(Compute Hours)

### 7. Add Filters

1. Click **"Add a control"** → **"Drop-down list"**
2. Configure:
   - **Control field**: Service
   - This allows filtering the entire dashboard by service

### 8. Create Calculated Fields

#### Average Cost per API Call

```
SUM(Calculated Cost USD) / SUM(API Calls)
```

#### Total Tokens (for Gemini)

```
Input Tokens + Output Tokens
```

#### Cost per Token

```
CASE
  WHEN Input Tokens + Output Tokens > 0 
  THEN Calculated Cost USD / (Input Tokens + Output Tokens)
  ELSE 0
END
```

## Sample Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Google Unified Dashboard - Usage & Costs                    │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│ Total Cost  │ API Calls   │ Storage GB  │ Compute Hours     │
│   $1,234    │   3,245     │   125.5 GB  │   85.5 hrs        │
├─────────────┴─────────────┴─────────────┴───────────────────┤
│                                                               │
│  ┌─────────────────┐      ┌───────────────────────────────┐ │
│  │ Cost by Service │      │   Cost Trend Over Time        │ │
│  │   (Pie Chart)   │      │     (Time Series)             │ │
│  │                 │      │                               │ │
│  └─────────────────┘      └───────────────────────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │        API Usage by Service (Bar Chart)                 │ │
│  │                                                          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─────────────────┐      ┌───────────────────────────────┐ │
│  │ Resource Usage  │      │   Detailed Metrics Table      │ │
│  │  (Gauge Charts) │      │                               │ │
│  └─────────────────┘      └───────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

1. **Use Date Ranges**: Add a date range control to allow filtering by time period
2. **Create Multiple Pages**: Organize different metric types on separate pages
3. **Apply Themes**: Use consistent colors and styling
4. **Add Annotations**: Include text boxes to explain key metrics
5. **Share Appropriately**: Set proper sharing permissions for your dashboard
6. **Refresh Regularly**: Data auto-refreshes, but you can manually refresh if needed

## Advanced Features

### Blended Data Sources

Combine the usage data with other data sources (e.g., budget data) to create variance reports.

### Email Reports

Schedule automatic email reports:
1. Click **"Share"** → **"Schedule email delivery"**
2. Set frequency and recipients

### Embedding

Embed dashboards in internal portals:
1. Click **"Share"** → **"Embed report"**
2. Copy the iframe code

## Troubleshooting

**Data not showing up**
- Verify the spreadsheet has data
- Check data source connection
- Refresh the data source

**Incorrect calculations**
- Verify field types in data source settings
- Check calculated field formulas

**Performance issues**
- Consider aggregating data before importing
- Limit date ranges
- Use data extracts for large datasets

## Example Dashboard Templates

You can use these pre-built visualizations as templates:

### Executive Summary Dashboard
- Total costs (monthly/quarterly)
- Cost trends
- Top 3 cost drivers
- Budget vs. actual

### Technical Operations Dashboard
- API call volumes
- Error rates (if tracked)
- Response times (if tracked)
- Resource utilization

### Financial Analysis Dashboard
- Cost breakdown by service
- Cost per unit metrics
- Forecast trends
- Cost optimization opportunities

## Resources

- [Looker Studio Documentation](https://support.google.com/looker-studio)
- [Looker Studio Community](https://www.en.advertisercommunity.com/t5/Looker-Studio/ct-p/looker-studio)
- [Data Studio Templates Gallery](https://datastudio.google.com/gallery)
