# Deployment Guide

This guide covers various deployment options for the Google Unified Dashboard.

## Deployment Options

1. **Local Machine** - For development and testing
2. **Cloud VM** - For production use
3. **Docker Container** - For containerized deployment
4. **Serverless** - Using cloud functions
5. **Process Manager** - Using PM2 for production

## 1. Local Development Deployment

### Prerequisites

- Node.js 14.x or higher
- npm or yarn
- Git

### Steps

```bash
# Clone repository
git clone https://github.com/ArtradePro/google-unified-dashboard.git
cd google-unified-dashboard

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Add Google credentials
# Place your credentials.json in project root

# Run the application
npm start
```

## 2. Cloud VM Deployment (GCP, AWS, Azure)

### Google Cloud Platform (GCP)

#### Create VM Instance

```bash
# Create a VM instance
gcloud compute instances create dashboard-vm \
  --machine-type=e2-micro \
  --zone=us-central1-a \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud

# SSH into instance
gcloud compute ssh dashboard-vm --zone=us-central1-a
```

#### Setup on VM

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Git
sudo apt-get install -y git

# Clone repository
git clone https://github.com/ArtradePro/google-unified-dashboard.git
cd google-unified-dashboard

# Install dependencies
npm install

# Configure application
nano .env
# Add your configuration

# Upload credentials
# Use gcloud compute scp to copy credentials.json
```

#### Run with PM2

```bash
# Install PM2
sudo npm install -g pm2

# Start application
pm2 start src/index.js --name google-dashboard

# Configure to start on boot
pm2 startup
pm2 save

# Monitor application
pm2 status
pm2 logs google-dashboard
```

### AWS EC2

#### Create EC2 Instance

1. Launch EC2 instance (t2.micro or higher)
2. Choose Ubuntu 22.04 LTS AMI
3. Configure security groups (no inbound needed for this app)
4. Create and download key pair

#### Setup on EC2

```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Follow similar steps as GCP setup above
```

### Azure VM

#### Create Azure VM

```bash
# Create resource group
az group create --name dashboard-rg --location eastus

# Create VM
az vm create \
  --resource-group dashboard-rg \
  --name dashboard-vm \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys

# Connect to VM
ssh azureuser@your-vm-ip

# Follow similar setup steps
```

## 3. Docker Deployment

### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application files
COPY src/ ./src/

# Create logs directory
RUN mkdir -p logs

# Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

USER nodejs

# Start application
CMD ["node", "src/index.js"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  dashboard:
    build: .
    container_name: google-unified-dashboard
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./credentials.json:/app/credentials.json:ro
      - ./logs:/app/logs
    environment:
      - NODE_ENV=production
```

### Build and Run

```bash
# Build image
docker build -t google-unified-dashboard .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 4. Serverless Deployment

### Google Cloud Functions

#### Prepare for Cloud Functions

Create `index.cloud.js`:

```javascript
const { AggregationService } = require('./src/services/aggregation');

exports.collectUsageData = async (req, res) => {
  try {
    const service = new AggregationService();
    await service.initialize();
    const result = await service.aggregate();
    
    res.status(200).json({
      success: true,
      summary: result.summary
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};
```

#### Deploy to Cloud Functions

```bash
# Deploy function
gcloud functions deploy collectUsageData \
  --runtime nodejs18 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --set-env-vars GOOGLE_SHEET_ID=your_sheet_id

# Create Cloud Scheduler job for periodic execution
gcloud scheduler jobs create http dashboard-collector \
  --schedule="0 * * * *" \
  --uri="https://REGION-PROJECT_ID.cloudfunctions.net/collectUsageData" \
  --http-method=GET
```

### AWS Lambda

#### Prepare Lambda Function

Create `lambda.js`:

```javascript
const { AggregationService } = require('./src/services/aggregation');

exports.handler = async (event) => {
  try {
    const service = new AggregationService();
    await service.initialize();
    const result = await service.aggregate();
    
    return {
      statusCode: 200,
      body: JSON.stringify(result)
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
```

#### Deploy with AWS SAM

Create `template.yaml`:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  DashboardFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: lambda.handler
      Runtime: nodejs18.x
      Timeout: 300
      Environment:
        Variables:
          GOOGLE_SHEET_ID: !Ref GoogleSheetId
      Events:
        Schedule:
          Type: Schedule
          Properties:
            Schedule: rate(1 hour)
```

## 5. PM2 Production Deployment

### PM2 Configuration

Create `ecosystem.config.js`:

```javascript
module.exports = {
  apps: [{
    name: 'google-dashboard',
    script: './src/index.js',
    instances: 1,
    exec_mode: 'fork',
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'production'
    },
    error_file: './logs/pm2-error.log',
    out_file: './logs/pm2-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
};
```

### PM2 Commands

```bash
# Start with config
pm2 start ecosystem.config.js

# Monitor
pm2 monit

# Logs
pm2 logs google-dashboard

# Restart
pm2 restart google-dashboard

# Stop
pm2 stop google-dashboard

# Save configuration
pm2 save

# Setup startup script
pm2 startup
```

## Environment-Specific Configuration

### Development

```env
NODE_ENV=development
LOG_LEVEL=debug
COLLECTION_INTERVAL_MINUTES=5
```

### Production

```env
NODE_ENV=production
LOG_LEVEL=info
COLLECTION_INTERVAL_MINUTES=60
```

## Monitoring and Logging

### Log Management

```bash
# Rotate logs with logrotate
sudo nano /etc/logrotate.d/google-dashboard
```

Add:

```
/path/to/google-unified-dashboard/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 nodejs nodejs
}
```

### Health Checks

Add health check endpoint (optional):

```javascript
// In src/index.js
const express = require('express');
const app = express();

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});

app.listen(3000);
```

### Monitoring Tools

- **PM2 Monitoring**: `pm2 monitor`
- **Cloud Monitoring**: GCP, AWS CloudWatch
- **Log aggregation**: ELK stack, Splunk
- **Uptime monitoring**: UptimeRobot, Pingdom

## Security Considerations

### Credentials Management

```bash
# Use Google Secret Manager (GCP)
gcloud secrets create google-dashboard-creds --data-file=./credentials.json

# Grant access to service account
gcloud secrets add-iam-policy-binding google-dashboard-creds \
  --member="serviceAccount:your-sa@project.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Network Security

- Use VPC for cloud deployments
- Implement firewall rules
- Enable HTTPS for API endpoints
- Use IAM roles instead of API keys where possible

### Regular Updates

```bash
# Update dependencies
npm update
npm audit fix

# Update Node.js
# Use nvm for version management
nvm install 18
nvm use 18
```

## Backup and Recovery

### Backup Configuration

```bash
# Backup environment and credentials
tar -czf backup-$(date +%Y%m%d).tar.gz .env credentials.json

# Store in secure location
# Google Cloud Storage, S3, etc.
```

### Disaster Recovery Plan

1. Keep configuration backed up
2. Document credentials location
3. Maintain runbook for deployment
4. Test recovery process regularly

## Scaling Considerations

### Horizontal Scaling

- Use load balancer for multiple instances
- Implement distributed locking for scheduled tasks
- Use message queue for data collection

### Vertical Scaling

- Increase VM/container resources
- Optimize collection intervals
- Batch API requests

## Troubleshooting Deployment

### Common Issues

**Issue: Module not found**
```bash
# Solution: Reinstall dependencies
rm -rf node_modules
npm install
```

**Issue: Permission denied**
```bash
# Solution: Fix permissions
sudo chown -R $USER:$USER /path/to/app
```

**Issue: Port already in use**
```bash
# Solution: Kill process or change port
lsof -ti:3000 | xargs kill -9
```

## Maintenance

### Regular Tasks

- Weekly: Review logs for errors
- Monthly: Update dependencies
- Quarterly: Rotate API keys
- Annually: Security audit

### Monitoring Checklist

- [ ] Application is running
- [ ] Data is being collected
- [ ] Google Sheets is updating
- [ ] No errors in logs
- [ ] Disk space available
- [ ] API rate limits not exceeded

## Support

For deployment issues:
1. Check logs first
2. Review troubleshooting section
3. Open GitHub issue with:
   - Deployment method
   - Error messages
   - Environment details

## Next Steps

1. Choose deployment method
2. Follow setup instructions
3. Configure monitoring
4. Test data collection
5. Set up alerts
6. Document your deployment

For more information, see the main README or other documentation files.
