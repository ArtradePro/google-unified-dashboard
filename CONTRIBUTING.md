# Contributing to Google Unified Dashboard

Thank you for your interest in contributing to the Google Unified Dashboard project! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear title and description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Node.js version, etc.)
- Relevant logs or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
- Use a clear and descriptive title
- Provide a detailed description of the proposed feature
- Explain why this enhancement would be useful
- Include examples of how it would work

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** as needed
5. **Write descriptive commit messages**
6. **Submit a pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/google-unified-dashboard.git
cd google-unified-dashboard

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Make your changes
# ...

# Test your changes
npm run test-apis
npm run mock-collect
```

## Coding Standards

### JavaScript Style Guide

- Use 2 spaces for indentation
- Use semicolons
- Use single quotes for strings
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused

### Example:

```javascript
// Good
async function collectData() {
  try {
    const result = await api.fetch();
    return result;
  } catch (error) {
    logger.error(`Failed to collect data: ${error.message}`);
    throw error;
  }
}

// Bad
async function cd(){
  return await api.fetch()
}
```

### File Structure

```
src/
├── collectors/     # Data collectors for each service
├── services/       # Core services (aggregation, Google Sheets)
├── utils/          # Utility functions and helpers
├── config.js       # Configuration management
└── index.js        # Main entry point
```

### Naming Conventions

- **Files**: Use camelCase for JavaScript files (e.g., `geminiCollector.js`)
- **Classes**: Use PascalCase (e.g., `GeminiCollector`)
- **Functions**: Use camelCase (e.g., `collectData`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`)

## Adding a New Service Collector

To add support for a new service:

1. Create a new collector file in `src/collectors/`:

```javascript
const axios = require('axios');
const logger = require('../utils/logger');
const config = require('../config');

class NewServiceCollector {
  constructor() {
    this.apiKey = config.newService.apiKey;
    this.apiUrl = config.newService.apiUrl;
  }

  async collect() {
    try {
      logger.info('Collecting NewService usage data...');
      
      if (!this.apiKey) {
        logger.warn('NewService API key not configured');
        return null;
      }

      const response = await axios.get(
        `${this.apiUrl}/usage`,
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`
          }
        }
      );

      return {
        service: 'NewService',
        timestamp: new Date().toISOString(),
        apiCalls: response.data.calls || 0,
        costs: response.data.cost || 0,
        status: 'success'
      };
    } catch (error) {
      logger.error(`Error collecting NewService data: ${error.message}`);
      return {
        service: 'NewService',
        timestamp: new Date().toISOString(),
        status: 'error',
        error: error.message
      };
    }
  }
}

module.exports = NewServiceCollector;
```

2. Add configuration in `src/config.js`:

```javascript
newService: {
  apiKey: process.env.NEW_SERVICE_API_KEY,
  apiUrl: process.env.NEW_SERVICE_API_URL || 'https://api.newservice.com'
}
```

3. Update `src/services/aggregation.js` to include the new collector:

```javascript
const NewServiceCollector = require('../collectors/newService');

// In constructor
this.collectors = [
  // ... existing collectors
  new NewServiceCollector()
];
```

4. Update `.env.example` with new environment variables
5. Update documentation in `docs/API_CONFIGURATION.md`

## Testing

Before submitting a pull request:

1. **Test API connectivity**:
```bash
npm run test-apis
```

2. **Test with mock data**:
```bash
npm run mock-collect
```

3. **Test the full application**:
```bash
npm start
# Ctrl+C to stop after verifying it works
```

4. **Check for errors in logs**:
```bash
cat logs/error.log
```

## Documentation

All significant changes should include documentation updates:

- Update `README.md` for user-facing changes
- Update `docs/` files for configuration changes
- Add inline code comments for complex logic
- Update API documentation for new endpoints

## Commit Messages

Use clear and descriptive commit messages:

```
Good:
- "Add support for NewService API collector"
- "Fix error handling in Google Sheets service"
- "Update README with deployment instructions"

Bad:
- "fix bug"
- "update code"
- "changes"
```

## Pull Request Process

1. **Update the README.md** with details of changes if needed
2. **Update the documentation** in `docs/` folder
3. **Add or update tests** for new functionality
4. **Ensure all checks pass**
5. **Request review** from maintainers

### PR Title Format

```
[Type] Brief description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- refactor: Code refactoring
- test: Test updates
- chore: Maintenance tasks
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Testing
Describe the testing you've done

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have tested my changes
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
```

## Getting Help

- Open an issue for questions
- Check existing issues and documentation first
- Provide context and details when asking for help

## Recognition

Contributors will be recognized in:
- Project README
- Release notes
- GitHub contributor list

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue with the `question` label if you have any questions about contributing!

Thank you for contributing to Google Unified Dashboard! 🎉
