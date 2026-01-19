require('dotenv').config();

const config = {
  googleSheets: {
    spreadsheetId: process.env.GOOGLE_SHEET_ID,
    credentials: process.env.GOOGLE_APPLICATION_CREDENTIALS
  },
  gemini: {
    apiKey: process.env.GEMINI_API_KEY,
    projectId: process.env.GEMINI_PROJECT_ID
  },
  opal: {
    apiKey: process.env.OPAL_API_KEY,
    apiUrl: process.env.OPAL_API_URL || 'https://api.opal.com'
  },
  wisk: {
    apiKey: process.env.WISK_API_KEY,
    apiUrl: process.env.WISK_API_URL || 'https://api.wisk.com'
  },
  polemi: {
    apiKey: process.env.POLEMI_API_KEY,
    apiUrl: process.env.POLEMI_API_URL || 'https://api.polemi.com'
  },
  collectionInterval: parseInt(process.env.COLLECTION_INTERVAL_MINUTES) || 60,
  logLevel: process.env.LOG_LEVEL || 'info'
};

module.exports = config;
