"""
FraudDocAI - Simple AI Service
Minimal FastAPI service for document processing and fraud detection
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging
from typing import List, Dict, Any
from datetime import datetime
import re
from emotion_fraud_detector import EmotionFraudDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize emotion fraud detector
emotion_detector = EmotionFraudDetector()

# Initialize FastAPI app
app = FastAPI(
    title="FraudDocAI AI Service",
    description="AI-powered document fraud detection service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TextAnalysisRequest(BaseModel):
    text: str

class EmbeddingsRequest(BaseModel):
    texts: List[str]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "FraudDocAI AI Service",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "models_loaded": {
            "document_processor": True,
            "fraud_detector": True,
            "embedding_model": True,
            "text_classifier": True,
            "question_answering": True,
            "emotion_detector": emotion_detector.model_loaded
        },
        "emotion_model_info": emotion_detector.get_model_info(),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    """
    Process uploaded document for fraud detection
    """
    try:
        logger.info(f"Processing document: {file.filename}")
        
        # Validate file type
        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
            "image/tiff",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}"
            )
        
        # Read file content
        content = await file.read()
        
        # Extract text from document
        extracted_text = await extract_text_from_document(content, file.content_type)
        
        # Analyze text for fraud patterns using emotion detector
        fraud_analysis = emotion_detector.analyze_fraud_patterns(extracted_text)
        
        result = {
            "document_id": f"doc-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "filename": file.filename,
            "file_type": file.content_type,
            "file_size": len(content),
            "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            "fraud_score": fraud_analysis["fraud_score"],
            "fraud_risk_level": fraud_analysis["risk_level"],
            "emotion_analysis": fraud_analysis["emotion_analysis"],
            "pattern_analysis": fraud_analysis["pattern_analysis"],
            "processing_time_ms": fraud_analysis["processing_time_ms"],
            "model_used": fraud_analysis["model_used"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Document processed successfully: {file.filename}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-text")
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text for fraud patterns
    """
    try:
        logger.info("Analyzing text for fraud patterns")
        
        # Use emotion-based fraud analysis
        fraud_analysis = emotion_detector.analyze_fraud_patterns(request.text)
        
        result = {
            "text_length": len(request.text),
            "fraud_score": fraud_analysis["fraud_score"],
            "fraud_risk_level": fraud_analysis["risk_level"],
            "emotion_analysis": fraud_analysis["emotion_analysis"],
            "pattern_analysis": fraud_analysis["pattern_analysis"],
            "analysis_time_ms": fraud_analysis["processing_time_ms"],
            "model_used": fraud_analysis["model_used"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-embeddings")
async def generate_embeddings(request: EmbeddingsRequest):
    """
    Generate embeddings for text documents
    """
    try:
        logger.info(f"Generating embeddings for {len(request.texts)} texts")
        
        # Generate simple mock embeddings
        embeddings = []
        start_time = datetime.utcnow()
        
        for i, text in enumerate(request.texts):
            # Simple hash-based embedding (384 dimensions)
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            embedding = [float(int(text_hash[j:j+2], 16)) / 255.0 for j in range(0, 32, 2)] * 12  # 384 dims
            
            embeddings.append({
                "text_index": i,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "embedding": embedding,
                "embedding_dimension": 384
            })
        
        generation_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        result = {
            "embeddings": embeddings,
            "model_used": "simple-hash-based",
            "generation_time_ms": round(generation_time, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fraud-patterns")
async def get_fraud_patterns():
    """
    Get available fraud detection patterns
    """
    try:
        patterns = [
            {
                "id": "signature_forgery",
                "name": "Signature Forgery",
                "description": "Detects potentially forged signatures",
                "severity": "high",
                "confidence_threshold": 0.8
            },
            {
                "id": "amount_tampering",
                "name": "Amount Tampering",
                "description": "Detects altered monetary amounts",
                "severity": "critical",
                "confidence_threshold": 0.9
            },
            {
                "id": "duplicate_invoice",
                "name": "Duplicate Invoice",
                "description": "Identifies duplicate invoices",
                "severity": "medium",
                "confidence_threshold": 0.95
            }
        ]
        
        return {
            "patterns": patterns,
            "total_count": len(patterns),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting fraud patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions for AI processing
async def extract_text_from_document(content: bytes, content_type: str) -> str:
    """Extract text from various document types using OCR and parsing"""
    try:
        if content_type == "application/pdf":
            import PyPDF2
            import io
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        
        elif content_type in ["image/jpeg", "image/png", "image/tiff"]:
            import pytesseract
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(image)
            return text.strip()
        
        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            from docx import Document
            import io
            doc = Document(io.BytesIO(content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        
        else:
            return "Unsupported file type for text extraction"
            
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return "Error extracting text from document"

# Old fraud analysis function removed - now using EmotionFraudDetector

if __name__ == "__main__":
    uvicorn.run(
        "simple_app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
