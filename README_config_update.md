### **4. Start AI Service**

#### **Default Configuration (No Setup Required)**
```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### **Custom Configuration Options**

**Using Environment Variables:**
```bash
# Change port
FRAUDDOCAI_PORT=9001 python app.py

# Change host and port
FRAUDDOCAI_HOST=127.0.0.1 FRAUDDOCAI_PORT=9001 python app.py

# Enable debug logging
FRAUDDOCAI_LOG_LEVEL=debug python app.py

# Production mode (no auto-reload)
FRAUDDOCAI_RELOAD=false python app.py
```

**Using Configuration File:**
```bash
# Copy example configuration
cp config.example.ini config.ini

# Edit configuration
nano config.ini

# Run with custom config
python app.py
```

#### **Available Configuration Options**

| Environment Variable | Description | Default | Example |
|---------------------|-------------|---------|---------|
| `FRAUDDOCAI_HOST` | Server host address | `0.0.0.0` | `127.0.0.1` |
| `FRAUDDOCAI_PORT` | Server port number | `8001` | `9001` |
| `FRAUDDOCAI_RELOAD` | Auto-reload on changes | `true` | `false` |
| `FRAUDDOCAI_LOG_LEVEL` | Log level | `info` | `debug` |
| `FRAUDDOCAI_CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:8080` | `https://myapp.com` |

**Note:** The AI service will automatically load Hugging Face models on startup. This may take 1-2 minutes on first run as models are downloaded and cached.

**📚 For detailed configuration options, see [CONFIGURATION.md](ai-service/CONFIGURATION.md)**
