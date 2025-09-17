# FraudDocAI Data Sourcing Guide

## 🎯 Overview
This guide provides comprehensive strategies for sourcing test data for the FraudDocAI system, including both synthetic and real-world datasets.

## 📊 Current System Analysis

### FraudDocAI Capabilities
- **Emotion-based fraud detection** using `cardiffnlp/twitter-roberta-base-emotion`
- **Pattern recognition** for fraud keywords and urgency indicators
- **Document Q&A** with `distilbert-base-uncased-distilled-squad`
- **Hybrid scoring** (40% emotion + 60% patterns)
- **Multi-format support** (TXT, PDF, JPG, PNG, TIFF, DOCX)

### Expected Fraud Score Ranges
- **High Risk**: 0.6-0.8 (Clear fraud indicators)
- **Medium Risk**: 0.3-0.5 (Suspicious patterns)
- **Low Risk**: 0.0-0.2 (Legitimate documents)

## 🔍 Data Sources

### 1. Synthetic Data Generation (Immediate Use)

#### A. Built-in Test Data Generator
```bash
cd FraudDocAI
python test_data_generator.py
```

**Features:**
- Generates 10 documents per risk level (30 total)
- Includes metadata and fraud indicators
- Covers multiple document types
- Realistic fraud patterns

#### B. Document Templates
- **Wire Transfer Requests**: Urgent payment scenarios
- **Invoice Documents**: Business invoices with fraud indicators
- **Bank Statements**: Account summaries with suspicious activity
- **Loan Applications**: Credit requests with various risk levels

### 2. Real-World Datasets (Free)

#### A. Credit Card Fraud Detection
- **Source**: Kaggle - "Credit Card Fraud Detection"
- **Size**: 284,807 transactions (492 fraudulent)
- **Download**: `kaggle datasets download -d mlg-ulb/creditcardfraud`
- **Use Case**: Transaction-based fraud patterns

#### B. Synthetic Financial Datasets
- **Source**: GitHub - "Synthetic Financial Datasets for Fraud Detection"
- **Repository**: `AnalystHarpal007/Synthetic-Financial-Datasets-For-Fraud-Detection`
- **Use Case**: Safe testing without privacy concerns

#### C. Document Processing Datasets
- **SROIE**: Receipt OCR and information extraction
- **CORD**: Complex document understanding
- **InvoiceNet**: Invoice processing and classification

### 3. API-Based Data Sources

#### A. Free Financial APIs
- **Alpha Vantage**: 5 API calls/minute, 500/day (free)
- **Yahoo Finance**: Free stock/financial data
- **Federal Reserve Economic Data (FRED)**: Free economic indicators

#### B. Open Banking APIs (Free Tiers)
- **Plaid**: 100 free API calls/month
- **Yodlee**: Free sandbox environment
- **Tink**: Free developer tier

## 🚀 Quick Start

### Step 1: Generate Synthetic Test Data
```bash
cd FraudDocAI
python test_data_generator.py
```

### Step 2: Download Real-World Datasets
```bash
# Install Kaggle API
pip install kaggle

# Download credit card fraud dataset
kaggle datasets download -d mlg-ulb/creditcardfraud
unzip creditcardfraud.zip

# Process the dataset
python download_datasets.py
```

### Step 3: Test with FraudDocAI
```bash
# Copy generated documents to test directory
cp test_documents_generated/*.txt backend/test_documents/

# Start the system
./scripts/start-dev.sh

# Test document upload and fraud detection
```

## 📋 Test Data Categories

### High Risk Documents (Expected 60-80% fraud score)
- Urgent wire transfer requests
- Fake invoices with fraud indicators
- Documents with multiple urgency keywords
- Offshore account references
- Confidentiality claims

### Medium Risk Documents (Expected 30-50% fraud score)
- Suspicious invoices
- Documents with some fraud indicators
- Unusual payment terms
- Wire transfer preferences

### Low Risk Documents (Expected 0-20% fraud score)
- Legitimate business invoices
- Standard payment terms
- Professional language
- Multiple payment options

## 🔧 Data Processing Pipeline

### 1. Document Generation
- Create realistic financial documents
- Include appropriate fraud indicators
- Generate metadata and expected scores

### 2. Data Validation
- Verify fraud score ranges
- Check document format compatibility
- Validate fraud indicator accuracy

### 3. System Integration
- Upload documents to FraudDocAI
- Test fraud detection accuracy
- Compare expected vs actual scores

## 📊 Testing Strategy

### Phase 1: Basic Testing
- Use existing test documents
- Validate system functionality
- Test all document types

### Phase 2: Synthetic Data
- Generate 100+ test documents
- Test various fraud scenarios
- Validate scoring accuracy

### Phase 3: Real-World Data
- Integrate public datasets
- Test with realistic data
- Validate production readiness

### Phase 4: Edge Cases
- Test extreme scenarios
- Validate error handling
- Test system limits

## 🎯 Success Metrics

### Fraud Detection Accuracy
- **High Risk Documents**: 80%+ correctly identified
- **Medium Risk Documents**: 70%+ correctly identified
- **Low Risk Documents**: 90%+ correctly identified

### System Performance
- **Processing Time**: <500ms per document
- **Throughput**: 100+ documents/minute
- **Accuracy**: 85%+ overall

## 📁 File Structure

```
FraudDocAI/
├── test_data_generator.py          # Synthetic data generation
├── download_datasets.py            # Real-world dataset downloader
├── test_documents_generated/       # Generated test documents
├── datasets/                       # Downloaded datasets
├── processed_datasets/             # Processed test data
└── backend/test_documents/         # System test documents
```

## 🔒 Privacy and Compliance

### Data Privacy
- Use synthetic data for development
- Anonymize any real data
- Implement data encryption
- Follow GDPR/HIPAA guidelines

### Best Practices
- Never use real customer data
- Use free tiers of commercial APIs
- Implement proper data handling
- Regular security audits

## 🚀 Next Steps

1. **Generate Test Data**: Run the test data generator
2. **Download Datasets**: Get real-world datasets
3. **Test System**: Validate fraud detection accuracy
4. **Iterate**: Improve based on test results
5. **Scale**: Prepare for production testing

## 📞 Support

For questions about data sourcing or testing:
- Check the generated metadata files
- Review the test data generator output
- Validate against expected fraud scores
- Test with your FraudDocAI system

---

*This guide provides comprehensive data sourcing strategies for FraudDocAI testing and validation.*
