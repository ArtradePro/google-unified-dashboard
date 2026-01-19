const logger = require('../utils/logger');
const GeminiCollector = require('../collectors/gemini');
const OpalCollector = require('../collectors/opal');
const WiskCollector = require('../collectors/wisk');
const PolemiCollector = require('../collectors/polemi');
const GoogleSheetsService = require('./googleSheets');

/**
 * Service to aggregate data from all collectors and write to Google Sheets
 */
class AggregationService {
  constructor() {
    this.collectors = [
      new GeminiCollector(),
      new OpalCollector(),
      new WiskCollector(),
      new PolemiCollector()
    ];
    this.sheetsService = new GoogleSheetsService();
  }

  /**
   * Initialize the aggregation service
   */
  async initialize() {
    try {
      await this.sheetsService.initialize();
      await this.sheetsService.setupSheets();
      logger.info('Aggregation service initialized');
    } catch (error) {
      logger.error(`Failed to initialize aggregation service: ${error.message}`);
      throw error;
    }
  }

  /**
   * Collect data from all sources
   */
  async collectAllData() {
    logger.info('Starting data collection from all sources...');
    
    const results = await Promise.all(
      this.collectors.map(collector => collector.collect())
    );

    logger.info(`Collected data from ${results.filter(r => r !== null).length} sources`);
    return results;
  }

  /**
   * Calculate summary statistics
   */
  calculateSummary(dataArray) {
    const validData = dataArray.filter(data => data !== null && data.status === 'success');
    
    return {
      totalApiCalls: validData.reduce((sum, data) => sum + (data.apiCalls || 0), 0),
      totalCosts: validData.reduce((sum, data) => sum + (data.costs || 0), 0),
      lastUpdated: new Date().toISOString(),
      servicesCount: validData.length
    };
  }

  /**
   * Run the full aggregation process
   */
  async aggregate() {
    try {
      logger.info('Starting aggregation process...');
      
      // Collect data from all sources
      const data = await this.collectAllData();
      
      // Write to Google Sheets
      await this.sheetsService.writeData(data);
      
      // Calculate and write summary
      const summary = this.calculateSummary(data);
      await this.sheetsService.writeSummary(summary);
      
      logger.info('Aggregation process completed successfully');
      logger.info(`Summary - API Calls: ${summary.totalApiCalls}, Costs: $${summary.totalCosts}`);
      
      return { success: true, summary };
    } catch (error) {
      logger.error(`Aggregation process failed: ${error.message}`);
      throw error;
    }
  }

  /**
   * Start continuous collection at specified interval
   */
  startScheduledCollection(intervalMinutes) {
    logger.info(`Starting scheduled collection every ${intervalMinutes} minutes`);
    
    // Run immediately
    this.aggregate().catch(error => {
      logger.error(`Initial aggregation failed: ${error.message}`);
    });

    // Then run on interval
    setInterval(() => {
      this.aggregate().catch(error => {
        logger.error(`Scheduled aggregation failed: ${error.message}`);
      });
    }, intervalMinutes * 60 * 1000);
  }
}

module.exports = AggregationService;
