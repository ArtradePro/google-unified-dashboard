# Quick Start Guide

Get the Google Unified Dashboard up and running in under 15 minutes!

## Prerequisites Checklist

- [ ] Node.js 14.x or higher installed
- [ ] npm or yarn installed
- [ ] Google Cloud account
- [ ] At least one API key (Gemini, Opal, Wisk, or Polemi)

## Step 1: Clone and Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/ArtradePro/google-unified-dashboard.git
cd google-unified-dashboard

# Install dependencies
npm install
```

## Step 2: Google Sheets Setup (5 minutes)

### Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it "Usage Dashboard"
4. Copy the spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
   ```

### Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable Google Sheets API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in details:
   - Name: `dashboard-collector`
   - Role: Select "Editor" (or create custom role)
4. Click "Done"
5. Click on the created service account
6. Go to "Keys" tab
7. Click "Add Key" > "Create new key"
8. Choose JSON format
9. Save the file as `credentials.json` in project root

### Share the Spreadsheet

1. Open your Google Sheet
2. Click "Share" button
3. Add the service account email (found in `credentials.json`)
4. Give "Editor" permissions
5. Click "Send"

## Step 3: Configure Environment (3 minutes)

```bash
# Copy environment template
cp .env.example .env
```

Edit `.env` file:

```env
# Required: Google Sheets
GOOGLE_SHEET_ID=paste_your_sheet_id_here
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

# Optional: Add at least one service API key
GEMINI_API_KEY=your_gemini_key_here
# OPAL_API_KEY=your_opal_key_here
# WISK_API_KEY=your_wisk_key_here
# POLEMI_API_KEY=your_polemi_key_here

# Collection interval (60 = every hour, 0 = run once)
COLLECTION_INTERVAL_MINUTES=60

# Logging
LOG_LEVEL=info
```

## Step 4: Test Configuration (2 minutes)

```bash
# Test API connectivity
npm run test-apis
```

Expected output:
```
✓ Google Sheets API: Connected successfully
✓ Gemini API: Connected successfully
⚠ Opal API key not configured
⚠ Wisk API key not configured
⚠ Polemi API key not configured

Test Summary
Passed: 2
Skipped/Failed: 3
```

## Step 5: Run First Collection (1 minute)

```bash
# Run once to test
COLLECTION_INTERVAL_MINUTES=0 npm start
```

Check your Google Sheet - you should see:
- "UsageData" sheet with collected data
- "Summary" sheet with aggregated metrics

## Step 6: Start Continuous Collection

```bash
# Start collecting data every hour
npm start

# Or use PM2 for production
npm install -g pm2
pm2 start src/index.js --name google-dashboard
pm2 save
```

## Step 7: Set Up Looker Studio (Optional, 5 minutes)

1. Go to [Looker Studio](https://lookerstudio.google.com/)
2. Click "Create" > "Data Source"
3. Select "Google Sheets"
4. Choose your spreadsheet
5. Select "UsageData" sheet
6. Click "Connect"
7. Create visualizations (see `docs/LOOKER_STUDIO_SETUP.md`)

## Troubleshooting

### Error: "Failed to initialize Google Sheets API"

**Solution**:
- Verify `credentials.json` exists
- Check service account has access to spreadsheet
- Ensure Google Sheets API is enabled

### Error: "GOOGLE_SHEET_ID not configured"

**Solution**:
- Check `.env` file exists
- Verify `GOOGLE_SHEET_ID` is set
- No spaces around the `=` sign

### No data in Google Sheets

**Solution**:
- Check logs: `cat logs/combined.log`
- Verify at least one API key is configured
- Ensure service account has "Editor" access

### "API key not valid" errors

**Solution**:
- Verify API keys are correct
- Check API keys haven't expired
- Ensure no extra spaces in `.env` file

## Next Steps

- **Configure more services**: Add API keys for other services
- **Adjust collection interval**: Modify `COLLECTION_INTERVAL_MINUTES`
- **Set up monitoring**: Create Looker Studio dashboard
- **Deploy to cloud**: See `docs/DEPLOYMENT.md`
- **Customize collectors**: Modify `src/collectors/` files

## Getting API Keys

### Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Add to `.env` as `GEMINI_API_KEY`

### Other Services
Refer to `docs/API_CONFIGURATION.md` for detailed instructions on:
- Opal API setup
- Wisk API setup
- Polemi API setup

## Common Commands

```bash
# Test API connectivity
npm run test-apis

# Run mock data collection (no real APIs)
npm run mock-collect

# Run once and exit
COLLECTION_INTERVAL_MINUTES=0 npm start

# Run continuously (every 60 minutes)
npm start

# View logs
tail -f logs/combined.log

# Stop PM2 service
pm2 stop google-dashboard
```

## Resource Links

- [Full Documentation](README.md)
- [API Configuration Guide](docs/API_CONFIGURATION.md)
- [Looker Studio Setup](docs/LOOKER_STUDIO_SETUP.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guide](CONTRIBUTING.md)

## Need Help?

- Check [README.md](README.md) for detailed information
- Review [docs/](docs/) folder for guides
- Open an issue on GitHub
- Run `npm run test-apis` to diagnose issues

## Success Checklist

- [ ] Dependencies installed
- [ ] Google Sheets created and shared
- [ ] Service account credentials configured
- [ ] At least one API key configured
- [ ] Test command passes
- [ ] First data collection successful
- [ ] Data visible in Google Sheets
- [ ] Application running continuously

Congratulations! Your Google Unified Dashboard is now running! 🎉
