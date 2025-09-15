# FraudDocAI
## Intelligent Financial Document Fraud Detection Platform

[![Go Version](https://img.shields.io/badge/Go-1.21-blue.svg)](https://golang.org/)
[![React Version](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Python Version](https://img.shields.io/badge/Python-3.12-green.svg)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com/)

> **FraudDocAI** is a complete fraud detection platform that combines modern web technologies with AI-powered document analysis to automatically detect fraudulent financial documents in real-time.

---

## 🎯 **Overview**

FraudDocAI helps businesses protect themselves from financial scams and document forgery by automatically analyzing uploaded documents for fraud patterns using machine learning models. The system provides real-time fraud detection with risk scoring and classification.

### **Key Features**
- 🔍 **Real-time Fraud Detection** - AI-powered analysis with instant results (40-500ms)
- 🧠 **Emotion-Based Analysis** - Hugging Face emotion model for psychological fraud detection
- 📊 **Risk Classification** - LOW, MEDIUM, HIGH, CRITICAL risk levels with confidence scores
- 🚀 **Modern UI/UX** - Professional drag-and-drop interface with emotion visualization
- 🔄 **Real-time Updates** - Live status updates during document processing
- 📁 **Multiple File Types** - Support for TXT, PDF, JPG, PNG, TIFF, DOCX
- 🏗️ **Microservices Architecture** - Scalable, production-ready design
- ❓ **Document Q&A** - Ask questions about documents and get AI-powered answers
- 📈 **Comprehensive Analysis** - Both emotion analysis and pattern detection
- 🔍 **Enhanced OCR** - Quality scoring, image preprocessing, and confidence indicators

---

## ✅ **Current Status: PRODUCTION-READY**

**Last Updated:** September 15, 2025

### **System Status:**
- **Frontend**: ✅ Running on port 3000 with complete UI
- **Backend**: ✅ Running on port 8080 with full API integration  
- **AI Service**: ✅ Running on port 8001 with emotion analysis
- **Database**: ✅ PostgreSQL with complete schema and data
- **Storage**: ✅ MinIO S3-compatible storage working
- **Document QA**: ✅ Question answering and fraud analysis working
- **Configuration**: ✅ Environment variable and config file support

### **Recent Achievements:**
- ✅ **Complete System Integration** - All microservices working seamlessly
- ✅ **Emotion-Based Fraud Detection** - Real Hugging Face model integration
- ✅ **Document Q&A Service** - AI-powered question answering working
- ✅ **Production-Ready System** - Robust error handling and service coordination
- ✅ **End-to-End Pipeline** - Complete document upload → analysis → storage → display
- ✅ **Enhanced OCR Quality** - Confidence scoring, image preprocessing, and quality indicators
- ✅ **Configuration Management** - Professional environment variable and config file system
- ✅ **Dynamic URL Building** - Eliminated hardcoded URLs for production deployment

---

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Frontend      │    │    Backend      │    │   AI Service     │
│   (React/TS)    │◄──►│   (Go/Gin)      │◄──►│ (Python/FastAPI) │
│   Port: 3000    │    │   Port: 8080    │    │   Port: 8001     │
└─────────────────┘    └─────────────────┘    └──────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   Port: 5432    │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │     MinIO       │
                       │   Port: 9000    │
                       └─────────────────┘
```

### **Technology Stack**
- **Frontend:** React 18, TypeScript, Tailwind CSS
- **Backend:** Go 1.21, Gin framework, PostgreSQL
- **AI Service:** Python 3.12, FastAPI, Hugging Face Transformers
- **Database:** PostgreSQL 14
- **Storage:** MinIO (S3-compatible)
- **Infrastructure:** Docker, Docker Compose

---

## 🚀 **Quick Start**

### **Prerequisites**
- Docker and Docker Compose
- Go 1.21+
- Node.js 18+
- Python 3.12+

### **1. Clone Repository**
```bash
git clone https://github.com/yourusername/frauddocai.git
cd frauddocai
```

### **2. Start Infrastructure Services**
```bash
docker-compose up -d
```

### **3. Start Backend**
```bash
cd backend
go mod download
go run main.go
```

### **4. Start AI Service**
```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Note:** The AI service will automatically load Hugging Face models on startup. This may take 1-2 minutes on first run as models are downloaded and cached.

### **5. Start Frontend**
```bash
cd frontend
npm install
npm start
```

### **6. Access Application**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8080
- **AI Service:** http://localhost:8001

---

## ⚙️ **Configuration**

FraudDocAI supports flexible configuration through environment variables and configuration files, making it production-ready for various deployment scenarios.

### **Environment Variables**

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `FRAUDDOCAI_HOST` | Server host address | `0.0.0.0` | `127.0.0.1` |
| `FRAUDDOCAI_PORT` | Server port number | `8001` | `9001` |
| `FRAUDDOCAI_RELOAD` | Auto-reload on changes | `true` | `false` |
| `FRAUDDOCAI_LOG_LEVEL` | Log level | `info` | `debug` |
| `FRAUDDOCAI_CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:8080` | `https://myapp.com` |
| `FRAUDDOCAI_EMOTION_MODEL` | Emotion analysis model | `cardiffnlp/twitter-roberta-base-emotion` | `microsoft/DialoGPT-medium` |
| `FRAUDDOCAI_QA_MODEL` | Question answering model | `distilbert-base-uncased-distilled-squad` | `deepset/roberta-base-squad2` |
| `FRAUDDOCAI_EMBEDDING_MODEL` | Embedding model | `all-MiniLM-L6-v2` | `all-mpnet-base-v2` |

### **Configuration File**

Create `config.ini` in the `ai-service` directory:

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

### **Dynamic URL Building**

```python
from config import config

# Get dynamic URLs based on configuration
base_url = config.get_base_url()        # http://0.0.0.0:8001
health_url = config.get_health_url()    # http://0.0.0.0:8001/health

# URLs automatically adapt to environment variables
# FRAUDDOCAI_PORT=9001 → http://0.0.0.0:9001
# FRAUDDOCAI_HOST=127.0.0.1 → http://127.0.0.1:8001
```

### **Production Deployment**

```bash
# Production configuration
FRAUDDOCAI_HOST=0.0.0.0 \
FRAUDDOCAI_PORT=8001 \
FRAUDDOCAI_RELOAD=false \
FRAUDDOCAI_LOG_LEVEL=warning \
python app.py
```

### **Docker Configuration**

```bash
# Docker with environment variables
docker run -e FRAUDDOCAI_PORT=8001 -e FRAUDDOCAI_HOST=0.0.0.0 frauddocai-ai

# Docker with config file
docker run -v ./config.ini:/app/config.ini frauddocai-ai
```

For detailed configuration options, see [CONFIGURATION.md](ai-service/CONFIGURATION.md).

---

## 🧪 **Demo & Testing**

### **Test Documents**
The system includes test documents with different fraud patterns:

```bash
cd backend/test_documents
ls -la *.txt
```

**Test Categories:**
- **HIGH RISK** - Wire transfer scams, fake invoices (60-80% fraud score)
- **MEDIUM RISK** - Suspicious invoices (30-50% fraud score)  
- **LOW RISK** - Legitimate business documents (0-20% fraud score)

### **Demo Workflow**
1. Upload `urgent_wire_transfer.txt` → Expect HIGH RISK (65-75%)
2. Upload `suspicious_invoice.txt` → Expect MEDIUM RISK (30-40%)
3. Upload `legitimate_invoice.txt` → Expect LOW RISK (5-15%)

---

## 🤖 **AI/ML Implementation**

### **Hybrid Fraud Detection System**
- **Emotion-Based Analysis:** Hugging Face `cardiffnlp/twitter-roberta-base-emotion` model
- **Document Q&A:** Hugging Face `distilbert-base-uncased-distilled-squad` model
- **Sentence Embeddings:** `all-MiniLM-L6-v2` for similarity search
- **Pattern-Based Analysis:** Keyword matching and regex pattern detection
- **Hybrid Scoring:** Combines emotion (40%) + pattern (60%) analysis
- **Real-Time Processing:** Sub-500ms fraud detection with confidence scoring

### **Emotion Analysis**
- **6 Emotions Detected:** anger, fear, joy, love, sadness, surprise
- **Fraud Indicators:** anger, fear, sadness (psychological manipulation)
- **Confidence Scoring:** Individual emotion confidence percentages
- **Visual Display:** Progress bars and emotion cards in UI

### **Detection Patterns**
- **Urgency Indicators** - "URGENT", "IMMEDIATE", "ASAP"
- **Confidentiality Claims** - "CONFIDENTIAL", "Do not share"
- **Payment Methods** - "Wire transfer only", "Offshore account"
- **Suspicious Amounts** - Large sums with urgency

### **OCR Quality Enhancement**
- **Confidence Scoring** - Real Tesseract confidence data analysis (0-100%)
- **Image Preprocessing** - Automatic contrast enhancement, noise reduction, and sharpening
- **Quality Levels** - Excellent (90%+), Good (70-89%), Fair (50-69%), Poor (<50%)
- **Visual Indicators** - Color-coded quality badges and progress bars in UI
- **User Guidance** - Clear feedback on when to re-upload documents for better results

### **Implementation Approach**
This system uses a **hybrid AI approach** that combines:
- **Hugging Face Models** - 3 real machine learning models:
  - `cardiffnlp/twitter-roberta-base-emotion` for emotion analysis
  - `distilbert-base-uncased-distilled-squad` for document Q&A
  - `all-MiniLM-L6-v2` for sentence embeddings
- **Pattern Recognition** - Keyword and regex-based fraud detection
- **Hybrid Scoring** - Emotion (40%) + Pattern (60%) fraud probability
- **Real-Time Processing** - Sub-500ms analysis with Apple Silicon GPU

**Benefits of Hybrid Approach:**
- 🧠 **Psychological Detection** - Identifies emotional manipulation tactics
- ⚡ **Fast Processing** - Sub-500ms response times
- 🎯 **High Accuracy** - Combines multiple detection methods
- 🔧 **Production Ready** - Robust error handling and monitoring

### **Risk Scoring**
- **0.0-0.3** - LOW RISK (Legitimate documents)
- **0.3-0.6** - MEDIUM RISK (Suspicious patterns)
- **0.6-1.0** - HIGH RISK (Clear fraud indicators)

---

## 🔧 **Technical Details**

### **API Endpoints**
- Document upload and management
- Real-time fraud analysis
- Health monitoring
- Document Q&A functionality

### **Database Design**
- PostgreSQL with JSONB for flexible data storage
- Optimized schema for fraud detection data
- Efficient indexing for performance

---

## 🔧 **Development**

### **Project Structure**
```
frauddocai/
├── frontend/            # React frontend application
├── backend/             # Go backend API
├── ai-service/          # Python AI service
├── database/            # Database schema and migrations
└── docker-compose.yml   # Infrastructure services
```

### **Quick Start**
```bash
# Start all services
./scripts/start-dev.sh

# Run tests
cd backend && go test ./...
cd frontend && npm test
cd ai-service && python -m pytest
```

---

## 📊 **Project Status**

### **Development Progress**
- **Week 1 (Sept 8-14)**: ✅ **COMPLETE** - Foundation & Core Features
- **Week 2 (Sept 15-21)**: ✅ **COMPLETE** - Advanced Features & Production Readiness
- **Week 3 (Sept 22-28)**: 🎯 **READY TO START** - Production Features
- **Week 4 (Sept 29-Oct 5)**: 🎯 **READY TO START** - Deployment & Portfolio

### **Current Capabilities**
- ✅ **Complete Fraud Detection Pipeline** - End-to-end document analysis
- ✅ **AI-Powered Analysis** - Hugging Face emotion models + pattern recognition
- ✅ **Multi-Format Support** - PDF, images, DOCX with OCR quality scoring
- ✅ **Production Configuration** - Environment variables and config files
- ✅ **Microservices Architecture** - Scalable, maintainable design
- ✅ **Real-time Processing** - Sub-500ms fraud analysis
- ✅ **Professional UI/UX** - Modern React interface with quality indicators

### **Technical Stack**
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Go 1.21 + Gin + PostgreSQL
- **AI Service**: Python 3.12 + FastAPI + Hugging Face
- **Storage**: MinIO S3-compatible object storage
- **Infrastructure**: Docker + Docker Compose

### **Next Phase Goals**
- **Advanced Analytics** - Historical fraud trends and reporting
- **Performance Monitoring** - Real-time system health and metrics
- **Cloud Deployment** - AWS/Azure/GCP production deployment
- **Portfolio Presentation** - Demo videos and case studies

---

## 👨‍💻 **Author**

**Jeremy Petty**
- Portfolio: https://medium.com/@jeremy.m.petty
- LinkedIn: https://www.linkedin.com/in/jeremympetty/

---

*This portfolio project demonstrates modern full-stack development, AI/ML integration, and production-ready software engineering practices.*