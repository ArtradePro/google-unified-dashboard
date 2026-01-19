# Example Deployment Configuration

This document provides examples for deploying the Google Unified Dashboard in various environments.

## Local Development

See [README.md](README.md) for local setup instructions.

## Cloud Deployment Options

### 1. Google Cloud Run (Scheduled Jobs)

Deploy as a Cloud Run job that runs on a schedule:

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/unified-dashboard', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/unified-dashboard']

# Deploy with Cloud Scheduler
# gcloud scheduler jobs create http dashboard-job \
#   --schedule="0 * * * *" \
#   --uri="https://REGION-PROJECT_ID.cloudfunctions.net/unified-dashboard" \
#   --http-method=POST
```

**Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### 2. AWS Lambda with EventBridge

Deploy as a Lambda function triggered by EventBridge (CloudWatch Events):

```python
# lambda_handler.py
import json
from main import UnifiedDashboard

def lambda_handler(event, context):
    dashboard = UnifiedDashboard()
    dashboard.run()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Dashboard execution completed')
    }
```

**EventBridge Rule**: Schedule expression `rate(1 hour)`

### 3. Azure Functions with Timer Trigger

```python
# __init__.py
import azure.functions as func
from main import UnifiedDashboard

def main(timer: func.TimerRequest) -> None:
    dashboard = UnifiedDashboard()
    dashboard.run()
```

**function.json**:
```json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "timer",
      "type": "timerTrigger",
      "direction": "in",
      "schedule": "0 0 * * * *"
    }
  ]
}
```

### 4. Kubernetes CronJob

```yaml
# cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: unified-dashboard
spec:
  schedule: "0 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: dashboard
            image: your-registry/unified-dashboard:latest
            env:
            - name: GEMINI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: gemini-key
            # Add other env vars
          restartPolicy: OnFailure
```

## Environment Variables Management

### Using Secret Manager (Recommended for Production)

**Google Cloud Secret Manager**:
```bash
# Create secrets
gcloud secrets create gemini-api-key --data-file=- <<< "your-key"

# Grant access to service account
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member="serviceAccount:YOUR-SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

**AWS Secrets Manager**:
```bash
aws secretsmanager create-secret \
  --name gemini-api-key \
  --secret-string "your-key"
```

**Azure Key Vault**:
```bash
az keyvault secret set \
  --vault-name your-vault \
  --name gemini-api-key \
  --value "your-key"
```

## Monitoring and Alerting

### Google Cloud Monitoring

```python
# Add to main.py
from google.cloud import monitoring_v3
import time

def write_metric(project_id, value):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    
    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/dashboard/records_processed"
    series.resource.type = "global"
    
    point = monitoring_v3.Point()
    point.value.int64_value = value
    point.interval.end_time.seconds = int(time.time())
    series.points = [point]
    
    client.create_time_series(name=project_name, time_series=[series])
```

### CloudWatch Metrics (AWS)

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_metric_data(
    Namespace='UnifiedDashboard',
    MetricData=[
        {
            'MetricName': 'RecordsProcessed',
            'Value': record_count,
            'Unit': 'Count'
        }
    ]
)
```

## High Availability Setup

For production environments:

1. **Multiple Regions**: Deploy in multiple regions for redundancy
2. **Retry Logic**: Implement exponential backoff for API calls
3. **Dead Letter Queues**: Handle failed executions
4. **Circuit Breakers**: Prevent cascading failures
5. **Health Checks**: Monitor service availability

## Cost Optimization

1. **Use spot/preemptible instances** for non-critical workloads
2. **Adjust collection frequency** based on needs
3. **Implement data retention policies** in Google Sheets
4. **Use connection pooling** for API calls
5. **Cache API responses** when appropriate

## Security Hardening

1. **Least Privilege**: Grant minimum necessary permissions
2. **Encrypt at Rest**: Enable encryption for all storage
3. **Network Security**: Use VPCs and private endpoints
4. **Audit Logging**: Enable cloud audit logs
5. **Regular Updates**: Keep dependencies updated

## Example Production Configuration

```yaml
# config.production.yaml
google_sheets:
  spreadsheet_name: "Production - Google Unified Dashboard"
  worksheet_name: "Usage Data"
  credentials_path: "/secrets/service-account.json"

aggregation:
  collection_interval: 30  # More frequent in production
  historical_days: 90
  timezone: "America/New_York"

# Enable all sources in production
sources:
  gemini:
    enabled: true
  opal:
    enabled: true
  wisk:
    enabled: true
  polemi:
    enabled: true
```

## Disaster Recovery

1. **Backup Strategy**:
   - Regular exports of Google Sheets data
   - Store backups in Cloud Storage/S3
   - Retention policy: 90 days

2. **Recovery Procedures**:
   - Document restore procedures
   - Test recovery regularly
   - Maintain runbooks

3. **Failover Plan**:
   - Alternative data collection paths
   - Manual execution procedures
   - Communication plan
