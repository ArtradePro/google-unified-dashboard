const logger = require('./utils/logger');
const config = require('./config');
const AggregationService = require('./services/aggregation');
const fs = require('fs');

/**
 * Main entry point for the Google Unified Dashboard
 */
async function main() {
  logger.info('Starting Google Unified Dashboard...');
  
  // Create logs directory if it doesn't exist
  if (!fs.existsSync('logs')) {
    fs.mkdirSync('logs');
  }

  try {
    // Validate configuration
    if (!config.googleSheets.spreadsheetId) {
      throw new Error('GOOGLE_SHEET_ID not configured in environment variables');
    }

    // Initialize aggregation service
    const aggregationService = new AggregationService();
    await aggregationService.initialize();

    // Check if running in continuous mode
    if (config.collectionInterval > 0) {
      logger.info(`Running in continuous mode with ${config.collectionInterval} minute interval`);
      aggregationService.startScheduledCollection(config.collectionInterval);
      
      // Keep process alive
      process.on('SIGINT', () => {
        logger.info('Received SIGINT, shutting down gracefully...');
        process.exit(0);
      });
      
      process.on('SIGTERM', () => {
        logger.info('Received SIGTERM, shutting down gracefully...');
        process.exit(0);
      });
    } else {
      // Run once and exit
      logger.info('Running in single execution mode');
      await aggregationService.aggregate();
      logger.info('Execution completed successfully');
      process.exit(0);
    }
  } catch (error) {
    logger.error(`Fatal error: ${error.message}`);
    logger.error(error.stack);
    process.exit(1);
  }
}

// Run the application
main();
