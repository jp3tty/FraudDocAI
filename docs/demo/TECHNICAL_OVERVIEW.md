# FraudDocAI Technical Overview
## Architecture & Implementation Details

---

## 🏗️ **System Architecture**

### **Microservices Design**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Service    │
│   (React/TS)    │◄──►│   (Go/Gin)      │◄──►│  (Python/FastAPI)│
│   Port: 3000    │    │   Port: 8080    │    │   Port: 8001    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
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
- **Frontend:** React 18, TypeScript, Tailwind CSS, React Query
- **Backend:** Go 1.21, Gin framework, PostgreSQL driver
- **AI Service:** Python 3.12, FastAPI, Hugging Face Transformers
- **Database:** PostgreSQL 14 with optimized schema
- **Storage:** MinIO (S3-compatible object storage)
- **Infrastructure:** Docker, Docker Compose

---

## 🔧 **Core Components**

### **1. Frontend (React/TypeScript)**
**Location:** `frontend/src/`

**Key Features:**
- **Document Upload:** Drag-and-drop interface with file validation
- **Real-time Updates:** Polling mechanism for fraud analysis results
- **Fraud Display:** Professional UI showing risk levels and scores
- **Responsive Design:** Mobile-friendly interface

**Key Files:**
- `pages/DocumentUpload.tsx` - Main upload interface with fraud results
- `services/api.ts` - API integration with backend
- `components/Navbar.tsx` - Navigation component

### **2. Backend (Go/Gin)**
**Location:** `backend/`

**Key Features:**
- **REST API:** Document upload, retrieval, and management
- **Database Integration:** PostgreSQL with connection pooling
- **File Storage:** MinIO integration for document persistence
- **AI Integration:** Automatic fraud analysis triggering

**Key Files:**
- `main.go` - Main application with API routes
- `services/database.go` - Database abstraction layer
- `config/minio.go` - Object storage configuration

### **3. AI Service (Python/FastAPI)**
**Location:** `ai-service/`

**Key Features:**
- **Fraud Detection:** Hugging Face models for pattern recognition
- **Text Analysis:** Keyword detection and risk scoring
- **Model Management:** Multiple ML models for different analysis types
- **Async Processing:** FastAPI for high-performance API

**Key Files:**
- `app.py` - Main AI service application with full OCR capabilities and authentication

### **4. Database (PostgreSQL)**
**Location:** `database/init.sql`

**Schema Design:**
- **documents** - Document metadata and fraud results
- **users** - User management and authentication
- **fraud_patterns** - Configurable fraud detection patterns
- **audit_logs** - System activity tracking

---

## 🤖 **AI/ML Implementation**

### **Fraud Detection Implementation**
- **Pattern-Based Analysis:** Advanced keyword matching and regex pattern detection
- **Risk Scoring Algorithm:** Multi-factor fraud probability calculation with confidence scoring
- **Real-Time Processing:** Fast, lightweight fraud detection engine with sub-millisecond response times

### **Fraud Detection Logic**
1. **Keyword Analysis** - Detect fraud-related terms with confidence scoring
2. **Pattern Recognition** - Identify suspicious document structures using regex patterns
3. **Multi-Factor Scoring** - Calculate fraud probability based on multiple indicators
4. **Risk Classification** - Assign risk levels (LOW, MEDIUM, HIGH, CRITICAL)
5. **Confidence Tracking** - Track detection confidence for each pattern

### **Detection Patterns**
- **Urgency Indicators** - "URGENT", "IMMEDIATE", "ASAP"
- **Confidentiality Claims** - "CONFIDENTIAL", "Do not share"
- **Payment Methods** - "Wire transfer only", "Offshore account"
- **Amount Patterns** - Large sums with urgency

---

## 📊 **Database Schema**

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
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Fraud Patterns Table**
```sql
CREATE TABLE fraud_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL,
    confidence_threshold DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔄 **Data Flow**

### **Document Processing Pipeline**
1. **Upload** - User uploads document via frontend
2. **Storage** - Document saved to MinIO object storage
3. **Metadata** - Document metadata stored in PostgreSQL
4. **Text Extraction** - Backend extracts text from document
5. **AI Analysis** - AI service analyzes text for fraud patterns
6. **Results Storage** - Fraud analysis results stored in database
7. **Frontend Update** - Real-time polling updates UI with results

### **API Endpoints**
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/` - List all documents
- `GET /api/v1/documents/:id` - Get specific document
- `POST /analyze-text` - AI fraud analysis endpoint

---

## 🚀 **Performance & Scalability**

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

## 🔒 **Security & Error Handling**

### **Security Measures**
- **Input Validation** - File type and size validation
- **SQL Injection Prevention** - Parameterized queries
- **CORS Configuration** - Cross-origin request handling
- **Error Sanitization** - Safe error messages

### **Error Handling**
- **Graceful Degradation** - System continues on component failure
- **Logging** - Comprehensive error logging
- **User Feedback** - Clear error messages in UI
- **Recovery** - Automatic retry mechanisms

---

## 📈 **Monitoring & Observability**

### **Health Checks**
- **Backend Health** - `GET /health` endpoint
- **AI Service Health** - Model loading status
- **Database Health** - Connection status
- **Storage Health** - MinIO availability

### **Logging**
- **Application Logs** - Structured logging in all services
- **Error Tracking** - Comprehensive error logging
- **Performance Metrics** - Response time tracking
- **Audit Trails** - Document processing history

---

## 🎯 **Key Technical Achievements**

1. **Full-Stack Integration** - Seamless frontend-backend-AI communication
2. **Real-time Processing** - Live fraud analysis with status updates
3. **Production Architecture** - Scalable, maintainable microservices
4. **AI Integration** - Machine learning models in production
5. **Database Design** - Optimized schema with proper relationships
6. **Error Handling** - Robust error handling and recovery
7. **Modern UI/UX** - Professional, responsive interface

---

*This technical overview demonstrates advanced full-stack development skills, AI integration, and production-ready system architecture.*
