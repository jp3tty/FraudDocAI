# FraudDocAI AI Service - Configuration Guide

This guide explains how to configure the FraudDocAI AI Service using environment variables and configuration files.

## 🚀 Quick Start

### Default Configuration (No Setup Required)
```bash
python app.py
# Runs on localhost:8001 with default settings
```

### Using Environment Variables
```bash
# Change port
FRAUDDOCAI_PORT=9001 python app.py

# Change host and port
FRAUDDOCAI_HOST=127.0.0.1 FRAUDDOCAI_PORT=9001 python app.py

# Change log level
FRAUDDOCAI_LOG_LEVEL=debug python app.py

# Disable reload for production
FRAUDDOCAI_RELOAD=false python app.py
```

### Using Configuration File
```bash
# Copy example config
cp config.example.ini config.ini

# Edit config.ini with your settings
nano config.ini

# Run with config file
python app.py
```

### Dynamic URL Building
```python
from config import config

# Get dynamic URLs based on configuration
base_url = config.get_base_url()        # http://0.0.0.0:8001
health_url = config.get_health_url()    # http://0.0.0.0:8001/health

# With custom protocol
https_url = config.get_base_url("https")  # https://0.0.0.0:8001

# URLs automatically adapt to environment variables
# FRAUDDOCAI_PORT=9001 → http://0.0.0.0:9001
# FRAUDDOCAI_HOST=127.0.0.1 → http://127.0.0.1:8001
```

## 📋 Configuration Options

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `FRAUDDOCAI_HOST` | Server host address | `0.0.0.0` | `127.0.0.1` |
| `FRAUDDOCAI_PORT` | Server port number | `8001` | `9001` |
| `FRAUDDOCAI_RELOAD` | Auto-reload on changes | `true` | `false` |
| `FRAUDDOCAI_LOG_LEVEL` | Log level | `info` | `debug` |
| `FRAUDDOCAI_CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:8080` | `https://myapp.com` |
| `FRAUDDOCAI_CORS_CREDENTIALS` | Allow CORS credentials | `true` | `false` |
| `FRAUDDOCAI_EMOTION_MODEL` | Emotion analysis model | `cardiffnlp/twitter-roberta-base-emotion` | `microsoft/DialoGPT-medium` |
| `FRAUDDOCAI_QA_MODEL` | Question answering model | `distilbert-base-uncased-distilled-squad` | `deepset/roberta-base-squad2` |
| `FRAUDDOCAI_EMBEDDING_MODEL` | Embedding model | `all-MiniLM-L6-v2` | `all-mpnet-base-v2` |
| `FRAUDDOCAI_CONFIG` | Path to config file | `config.ini` | `/path/to/my-config.ini` |

### Configuration File (config.ini)

```ini
[server]
host = 0.0.0.0
port = 8001
reload = true
log_level = info

[cors]
allowed_origins = http://localhost:3000,http://localhost:8080
allow_credentials = true

[ai]
emotion_model = cardiffnlp/twitter-roberta-base-emotion
qa_model = distilbert-base-uncased-distilled-squad
embedding_model = all-MiniLM-L6-v2
```

## 🔧 Usage Examples

### Development Setup
```bash
# Use default settings
python app.py

# Enable debug logging
FRAUDDOCAI_LOG_LEVEL=debug python app.py

# Use different port
FRAUDDOCAI_PORT=8000 python app.py
```

### Production Setup
```bash
# Disable auto-reload
FRAUDDOCAI_RELOAD=false python app.py

# Use production log level
FRAUDDOCAI_LOG_LEVEL=warning python app.py

# Use specific host
FRAUDDOCAI_HOST=0.0.0.0 python app.py
```

### Docker Setup
```bash
# Set environment variables
docker run -e FRAUDDOCAI_PORT=8001 -e FRAUDDOCAI_HOST=0.0.0.0 frauddocai-ai

# Use config file
docker run -v ./config.ini:/app/config.ini frauddocai-ai
```

### Kubernetes Setup
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frauddocai-ai
spec:
  template:
    spec:
      containers:
      - name: ai-service
        image: frauddocai-ai
        env:
        - name: FRAUDDOCAI_PORT
          value: "8001"
        - name: FRAUDDOCAI_HOST
          value: "0.0.0.0"
        - name: FRAUDDOCAI_RELOAD
          value: "false"
```

## 🎯 Configuration Priority

Configuration is applied in this order (later overrides earlier):

1. **Default values** (hardcoded in config.py)
2. **Configuration file** (config.ini)
3. **Environment variables** (highest priority)

## 🔍 Verification

### Check Current Configuration
```bash
# Get configuration via API
curl http://localhost:8001/health

# Response includes current configuration
{
  "status": "healthy",
  "configuration": {
    "server": {
      "host": "0.0.0.0",
      "port": 8001,
      "reload": true,
      "log_level": "info"
    },
    "cors": {
      "allow_origins": ["http://localhost:3000", "http://localhost:8080"],
      "allow_credentials": true
    },
    "ai": {
      "emotion_model": "cardiffnlp/twitter-roberta-base-emotion",
      "qa_model": "distilbert-base-uncased-distilled-squad",
      "embedding_model": "all-MiniLM-L6-v2"
    }
  }
}
```

### Test Configuration
```bash
# Test with different port
FRAUDDOCAI_PORT=9001 python app.py &
curl http://localhost:9001/health

# Test with different host
FRAUDDOCAI_HOST=127.0.0.1 python app.py &
curl http://127.0.0.1:8001/health
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Use different port
   FRAUDDOCAI_PORT=9001 python app.py
   ```

2. **CORS errors**
   ```bash
   # Add your frontend URL to CORS origins
   FRAUDDOCAI_CORS_ORIGINS="http://localhost:3000,https://myapp.com" python app.py
   ```

3. **Model loading fails**
   ```bash
   # Check model names are correct
   FRAUDDOCAI_EMOTION_MODEL="cardiffnlp/twitter-roberta-base-emotion" python app.py
   ```

4. **Configuration file not found**
   ```bash
   # Specify full path to config file
   FRAUDDOCAI_CONFIG="/full/path/to/config.ini" python app.py
   ```

### Debug Mode
```bash
# Enable debug logging to see configuration loading
FRAUDDOCAI_LOG_LEVEL=debug python app.py
```

## 📚 Advanced Configuration

### Custom Model Configuration
```bash
# Use different models
FRAUDDOCAI_EMOTION_MODEL="microsoft/DialoGPT-medium" \
FRAUDDOCAI_QA_MODEL="deepset/roberta-base-squad2" \
FRAUDDOCAI_EMBEDDING_MODEL="all-mpnet-base-v2" \
python app.py
```

### Multiple Environment Setup
```bash
# Development
FRAUDDOCAI_PORT=8001 FRAUDDOCAI_LOG_LEVEL=debug python app.py

# Staging
FRAUDDOCAI_PORT=8002 FRAUDDOCAI_LOG_LEVEL=info python app.py

# Production
FRAUDDOCAI_PORT=8003 FRAUDDOCAI_LOG_LEVEL=warning FRAUDDOCAI_RELOAD=false python app.py
```

### Configuration Validation
The service will log the configuration on startup:
```
INFO: Starting FraudDocAI AI Service with configuration:
INFO:   Host: 0.0.0.0
INFO:   Port: 8001
INFO:   Reload: true
INFO:   Log Level: info
```

This ensures your configuration is applied correctly!
