/**
 * Example of creating a mock data collector for testing
 * Useful for testing the dashboard without real API credentials
 */

const logger = require('../src/utils/logger');

class MockCollector {
  constructor(serviceName) {
    this.serviceName = serviceName;
  }

  /**
   * Generate mock usage data
   * @returns {Promise<Object>} Mock usage data
   */
  async collect() {
    logger.info(`Collecting mock data for ${this.serviceName}...`);

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Generate random metrics
    const apiCalls = Math.floor(Math.random() * 10000) + 1000;
    const costs = (Math.random() * 100).toFixed(2);

    const mockData = {
      service: this.serviceName,
      timestamp: new Date().toISOString(),
      apiCalls: apiCalls,
      costs: parseFloat(costs),
      status: 'success',
      // Service-specific mock data
      ...(this.serviceName === 'Gemini' && {
        tokenUsage: Math.floor(Math.random() * 1000000),
        modelsUsed: ['gemini-pro', 'gemini-pro-vision']
      }),
      ...(this.serviceName === 'Opal' && {
        resources: { users: 50, groups: 10 },
        activeUsers: Math.floor(Math.random() * 50)
      }),
      ...(this.serviceName === 'Wisk' && {
        bandwidth: (Math.random() * 1000).toFixed(2),
        storage: (Math.random() * 500).toFixed(2)
      }),
      ...(this.serviceName === 'Polemi' && {
        computeHours: (Math.random() * 100).toFixed(2),
        dataProcessed: (Math.random() * 1000).toFixed(2)
      })
    };

    logger.info(`Mock data collected for ${this.serviceName}: ${apiCalls} API calls`);
    return mockData;
  }
}

/**
 * Example: Using mock collectors for testing
 */
async function runMockCollection() {
  const mockCollectors = [
    new MockCollector('Gemini'),
    new MockCollector('Opal'),
    new MockCollector('Wisk'),
    new MockCollector('Polemi')
  ];

  console.log('Starting mock data collection...\n');

  const results = await Promise.all(
    mockCollectors.map(collector => collector.collect())
  );

  console.log('\nMock Data Results:');
  console.log(JSON.stringify(results, null, 2));

  // Calculate summary
  const summary = {
    totalApiCalls: results.reduce((sum, r) => sum + r.apiCalls, 0),
    totalCosts: results.reduce((sum, r) => sum + r.costs, 0),
    servicesCount: results.length,
    timestamp: new Date().toISOString()
  };

  console.log('\nSummary:');
  console.log(JSON.stringify(summary, null, 2));
}

// Run if executed directly
if (require.main === module) {
  runMockCollection().catch(console.error);
}

module.exports = MockCollector;
