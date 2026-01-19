const { google } = require('googleapis');
const logger = require('../utils/logger');
const config = require('../config');
const fs = require('fs');

/**
 * Service for writing data to Google Sheets
 */
class GoogleSheetsService {
  constructor() {
    this.spreadsheetId = config.googleSheets.spreadsheetId;
    this.auth = null;
    this.sheets = null;
  }

  /**
   * Initialize Google Sheets API authentication
   */
  async initialize() {
    try {
      logger.info('Initializing Google Sheets API...');
      
      if (!config.googleSheets.credentials) {
        throw new Error('Google credentials file path not configured');
      }

      if (!fs.existsSync(config.googleSheets.credentials)) {
        throw new Error(`Credentials file not found: ${config.googleSheets.credentials}`);
      }

      const credentials = JSON.parse(fs.readFileSync(config.googleSheets.credentials, 'utf8'));
      
      this.auth = new google.auth.GoogleAuth({
        credentials: credentials,
        scopes: ['https://www.googleapis.com/auth/spreadsheets']
      });

      this.sheets = google.sheets({ version: 'v4', auth: this.auth });
      logger.info('Google Sheets API initialized successfully');
    } catch (error) {
      logger.error(`Failed to initialize Google Sheets API: ${error.message}`);
      throw error;
    }
  }

  /**
   * Create or update sheet structure
   */
  async setupSheets() {
    try {
      logger.info('Setting up sheet structure...');

      // Create headers for the main data sheet
      const headers = [
        ['Timestamp', 'Service', 'API Calls', 'Costs ($)', 'Status', 'Additional Metrics', 'Error']
      ];

      await this.sheets.spreadsheets.values.update({
        spreadsheetId: this.spreadsheetId,
        range: 'UsageData!A1:G1',
        valueInputOption: 'RAW',
        resource: {
          values: headers
        }
      });

      logger.info('Sheet structure setup complete');
    } catch (error) {
      logger.error(`Error setting up sheets: ${error.message}`);
      throw error;
    }
  }

  /**
   * Write usage data to Google Sheets
   * @param {Array} dataArray - Array of usage data objects
   */
  async writeData(dataArray) {
    try {
      logger.info(`Writing ${dataArray.length} records to Google Sheets...`);

      const rows = dataArray
        .filter(data => data !== null)
        .map(data => {
          // Filter out null/undefined values before stringifying
          const additionalMetrics = {};
          const fields = ['tokenUsage', 'modelsUsed', 'resources', 'activeUsers', 
                         'bandwidth', 'storage', 'computeHours', 'dataProcessed'];
          
          fields.forEach(field => {
            if (data[field] !== undefined && data[field] !== null) {
              additionalMetrics[field] = data[field];
            }
          });

          return [
            data.timestamp,
            data.service,
            data.apiCalls || 0,
            data.costs || 0,
            data.status,
            Object.keys(additionalMetrics).length > 0 ? JSON.stringify(additionalMetrics) : '',
            data.error || ''
          ];
        });

      if (rows.length === 0) {
        logger.warn('No data to write to sheets');
        return;
      }

      await this.sheets.spreadsheets.values.append({
        spreadsheetId: this.spreadsheetId,
        range: 'UsageData!A:G',
        valueInputOption: 'RAW',
        insertDataOption: 'INSERT_ROWS',
        resource: {
          values: rows
        }
      });

      logger.info(`Successfully wrote ${rows.length} rows to Google Sheets`);
    } catch (error) {
      logger.error(`Error writing data to Google Sheets: ${error.message}`);
      throw error;
    }
  }

  /**
   * Create summary sheet with aggregated data
   */
  async writeSummary(summaryData) {
    try {
      logger.info('Writing summary data...');

      const summaryRows = [
        ['Metric', 'Value'],
        ['Total API Calls', summaryData.totalApiCalls],
        ['Total Costs ($)', summaryData.totalCosts],
        ['Last Updated', summaryData.lastUpdated],
        ['Services Monitored', summaryData.servicesCount]
      ];

      await this.sheets.spreadsheets.values.update({
        spreadsheetId: this.spreadsheetId,
        range: 'Summary!A1:B5',
        valueInputOption: 'RAW',
        resource: {
          values: summaryRows
        }
      });

      logger.info('Summary data written successfully');
    } catch (error) {
      logger.error(`Error writing summary: ${error.message}`);
      throw error;
    }
  }
}

module.exports = GoogleSheetsService;
