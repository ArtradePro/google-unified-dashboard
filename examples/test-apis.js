/**
 * Example script to test API connectivity for all services
 * Run this before setting up the full dashboard to verify your API credentials
 */

require('dotenv').config();
const axios = require('axios');

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m'
};

async function testGeminiAPI() {
  console.log(`\n${colors.blue}Testing Gemini API...${colors.reset}`);
  
  if (!process.env.GEMINI_API_KEY) {
    console.log(`${colors.yellow}⚠ Gemini API key not configured${colors.reset}`);
    return false;
  }

  try {
    const response = await axios.get(
      'https://generativelanguage.googleapis.com/v1/models',
      {
        headers: {
          'Authorization': `Bearer ${process.env.GEMINI_API_KEY}`
        },
        timeout: 5000
      }
    );
    
    console.log(`${colors.green}✓ Gemini API: Connected successfully${colors.reset}`);
    return true;
  } catch (error) {
    console.log(`${colors.red}✗ Gemini API: Failed - ${error.message}${colors.reset}`);
    if (error.response) {
      console.log(`  Status: ${error.response.status}`);
      console.log(`  Message: ${error.response.data.error?.message || 'Unknown error'}`);
    }
    return false;
  }
}

async function testOpalAPI() {
  console.log(`\n${colors.blue}Testing Opal API...${colors.reset}`);
  
  if (!process.env.OPAL_API_KEY) {
    console.log(`${colors.yellow}⚠ Opal API key not configured${colors.reset}`);
    return false;
  }

  try {
    const apiUrl = process.env.OPAL_API_URL || 'https://api.opal.com';
    const response = await axios.get(
      `${apiUrl}/usage`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPAL_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 5000
      }
    );
    
    console.log(`${colors.green}✓ Opal API: Connected successfully${colors.reset}`);
    return true;
  } catch (error) {
    console.log(`${colors.red}✗ Opal API: Failed - ${error.message}${colors.reset}`);
    if (error.response) {
      console.log(`  Status: ${error.response.status}`);
    }
    return false;
  }
}

async function testWiskAPI() {
  console.log(`\n${colors.blue}Testing Wisk API...${colors.reset}`);
  
  if (!process.env.WISK_API_KEY) {
    console.log(`${colors.yellow}⚠ Wisk API key not configured${colors.reset}`);
    return false;
  }

  try {
    const apiUrl = process.env.WISK_API_URL || 'https://api.wisk.com';
    const response = await axios.get(
      `${apiUrl}/analytics/usage`,
      {
        headers: {
          'X-API-Key': process.env.WISK_API_KEY,
          'Content-Type': 'application/json'
        },
        timeout: 5000
      }
    );
    
    console.log(`${colors.green}✓ Wisk API: Connected successfully${colors.reset}`);
    return true;
  } catch (error) {
    console.log(`${colors.red}✗ Wisk API: Failed - ${error.message}${colors.reset}`);
    if (error.response) {
      console.log(`  Status: ${error.response.status}`);
    }
    return false;
  }
}

async function testPolemiAPI() {
  console.log(`\n${colors.blue}Testing Polemi API...${colors.reset}`);
  
  if (!process.env.POLEMI_API_KEY) {
    console.log(`${colors.yellow}⚠ Polemi API key not configured${colors.reset}`);
    return false;
  }

  try {
    const apiUrl = process.env.POLEMI_API_URL || 'https://api.polemi.com';
    const response = await axios.get(
      `${apiUrl}/v1/usage`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.POLEMI_API_KEY}`,
          'Accept': 'application/json'
        },
        timeout: 5000
      }
    );
    
    console.log(`${colors.green}✓ Polemi API: Connected successfully${colors.reset}`);
    return true;
  } catch (error) {
    console.log(`${colors.red}✗ Polemi API: Failed - ${error.message}${colors.reset}`);
    if (error.response) {
      console.log(`  Status: ${error.response.status}`);
    }
    return false;
  }
}

async function testGoogleSheets() {
  console.log(`\n${colors.blue}Testing Google Sheets API...${colors.reset}`);
  
  if (!process.env.GOOGLE_SHEET_ID) {
    console.log(`${colors.red}✗ GOOGLE_SHEET_ID not configured${colors.reset}`);
    return false;
  }

  if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
    console.log(`${colors.red}✗ GOOGLE_APPLICATION_CREDENTIALS not configured${colors.reset}`);
    return false;
  }

  try {
    const fs = require('fs');
    const { google } = require('googleapis');
    
    if (!fs.existsSync(process.env.GOOGLE_APPLICATION_CREDENTIALS)) {
      console.log(`${colors.red}✗ Credentials file not found: ${process.env.GOOGLE_APPLICATION_CREDENTIALS}${colors.reset}`);
      return false;
    }

    const credentials = JSON.parse(fs.readFileSync(process.env.GOOGLE_APPLICATION_CREDENTIALS, 'utf8'));
    
    const auth = new google.auth.GoogleAuth({
      credentials: credentials,
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    });

    const sheets = google.sheets({ version: 'v4', auth });
    
    // Try to read the spreadsheet
    await sheets.spreadsheets.get({
      spreadsheetId: process.env.GOOGLE_SHEET_ID
    });
    
    console.log(`${colors.green}✓ Google Sheets API: Connected successfully${colors.reset}`);
    console.log(`  Spreadsheet ID: ${process.env.GOOGLE_SHEET_ID}`);
    return true;
  } catch (error) {
    console.log(`${colors.red}✗ Google Sheets API: Failed - ${error.message}${colors.reset}`);
    return false;
  }
}

async function runTests() {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`${colors.blue}Google Unified Dashboard - API Connectivity Test${colors.reset}`);
  console.log(`${'='.repeat(60)}`);

  const results = {
    googleSheets: await testGoogleSheets(),
    gemini: await testGeminiAPI(),
    opal: await testOpalAPI(),
    wisk: await testWiskAPI(),
    polemi: await testPolemiAPI()
  };

  console.log(`\n${'='.repeat(60)}`);
  console.log(`${colors.blue}Test Summary${colors.reset}`);
  console.log(`${'='.repeat(60)}\n`);

  const total = Object.keys(results).length;
  const passed = Object.values(results).filter(r => r === true).length;
  const skipped = Object.values(results).filter(r => r === false).length;

  console.log(`Total tests: ${total}`);
  console.log(`${colors.green}Passed: ${passed}${colors.reset}`);
  console.log(`${colors.yellow}Skipped/Failed: ${skipped}${colors.reset}`);

  if (results.googleSheets) {
    console.log(`\n${colors.green}✓ Core functionality ready (Google Sheets connected)${colors.reset}`);
    console.log(`${colors.yellow}Configure at least one service API key to start collecting data${colors.reset}`);
  } else {
    console.log(`\n${colors.red}✗ Google Sheets not configured - this is required${colors.reset}`);
    console.log(`${colors.yellow}Please set up Google Sheets API credentials first${colors.reset}`);
  }

  console.log(`\n${'='.repeat(60)}\n`);
}

// Run tests
runTests().catch(error => {
  console.error(`${colors.red}Fatal error: ${error.message}${colors.reset}`);
  process.exit(1);
});
