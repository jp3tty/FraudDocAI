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

## ✅ **Current Status: FULLY OPERATIONAL**

**Last Updated:** September 14, 2025

### **System Status:**
- **Frontend**: ✅ Running on port 3000 with complete UI
- **Backend**: ✅ Running on port 8080 with full API integration  
- **AI Service**: ✅ Running on port 8001 with emotion analysis
- **Database**: ✅ PostgreSQL with complete schema and data
- **Storage**: ✅ MinIO S3-compatible storage working
- **Document QA**: ✅ Question answering and fraud analysis working

### **Recent Achievements:**
- ✅ **Complete System Integration** - All microservices working seamlessly
- ✅ **Emotion-Based Fraud Detection** - Real Hugging Face model integration
- ✅ **Document Q&A Service** - AI-powered question answering working
- ✅ **Production-Ready System** - Robust error handling and service coordination
- ✅ **End-to-End Pipeline** - Complete document upload → analysis → storage → display
- ✅ **Enhanced OCR Quality** - Confidence scoring, image preprocessing, and quality indicators

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

## 📊 **API Documentation**

### **Document Management**
```bash
# Upload document
POST /api/v1/documents/upload
Content-Type: multipart/form-data

# Get all documents
GET /api/v1/documents/

# Get specific document
GET /api/v1/documents/:id
```

### **Fraud Analysis**
```bash
# Analyze text for fraud
POST /analyze-text
Content-Type: application/json
{
  "text": "URGENT: Please wire transfer $50,000..."
}
```

### **Health Checks**
```bash
# Backend health
GET /health

# AI service health
GET /health
```

---

## 🗄️ **Database Schema**

### **Documents Table**
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    mime_type VARCHAR(100),
    document_type VARCHAR(100),
    status VARCHAR(50) DEFAULT 'uploaded',
    fraud_score DECIMAL(3,2),
    fraud_risk_level VARCHAR(20) DEFAULT 'low',
    extracted_text TEXT,
    emotion_analysis JSONB,
    pattern_analysis JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Emotion Analysis JSONB Structure**
```json
{
  "emotions": [
    {"emotion": "joy", "confidence": 0.707},
    {"emotion": "anger", "confidence": 0.084}
  ],
  "fraud_indicators": [
    {
      "emotion": "anger",
      "confidence": 0.084,
      "reason": "Anger can indicate frustration or manipulation"
    }
  ],
  "emotion_fraud_score": 0.0,
  "model_used": "cardiffnlp/twitter-roberta-base-emotion"
}
```

---

## 🔧 **Development**

### **Project Structure**
```
frauddocai/
├── frontend/          # React frontend application
├── backend/           # Go backend API
├── ai-service/        # Python AI service
├── database/          # Database schema and migrations
├── docs/             # Documentation and demo materials
├── scripts/          # Development and deployment scripts
└── docker-compose.yml # Infrastructure services
```

### **Key Commands**
```bash
# Start all services
./scripts/start-dev.sh

# Stop all services
./scripts/stop-dev.sh

# Run tests
cd backend && go test ./...
cd frontend && npm test
cd ai-service && python -m pytest
```

---

## 📈 **Performance & Scalability**

### **Optimizations**
- **Database Indexing** - Optimized queries with proper indexes
- **Connection Pooling** - Efficient database connections
- **Async Processing** - Background fraud analysis
- **Caching** - MinIO for document storage

### **Scalability Features**
- **Microservices** - Independent scaling of components
- **Docker** - Containerized deployment
- **Database Design** - Normalized schema for performance
- **API Design** - RESTful endpoints for integration

---

## 🔒 **Security**

### **Security Measures**
- **Input Validation** - File type and size validation
- **SQL Injection Prevention** - Parameterized queries
- **CORS Configuration** - Cross-origin request handling
- **Error Sanitization** - Safe error messages

---

## 📝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **Author**

**Jeremy Petty**
- Portfolio: https://medium.com/@jeremy.m.petty
- LinkedIn: https://www.linkedin.com/in/jeremympetty/

---

## 🙏 **Acknowledgments**

- [Hugging Face](https://huggingface.co/) for pre-trained models
- [React](https://reactjs.org/) for the frontend framework
- [Go](https://golang.org/) for the backend language
- [FastAPI](https://fastapi.tiangolo.com/) for the AI service framework

---

## 📊 **Project Statistics**

- **Lines of Code:** ~3,000+
- **Technologies Used:** 10+ (including Hugging Face)
- **AI Models:** 3 (cardiffnlp/twitter-roberta-base-emotion, distilbert-base-uncased-distilled-squad, all-MiniLM-L6-v2)
- **Services:** 3 microservices
- **Database Tables:** 6 (with JSONB fields)
- **API Endpoints:** 12+
- **Test Coverage:** 85%+

---

*FraudDocAI demonstrates advanced full-stack development skills, AI integration, and production-ready system architecture.*