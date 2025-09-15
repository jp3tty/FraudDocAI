"""
FraudDocAI - AI Service
FastAPI service for document processing and fraud detection
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import logging
from typing import List, Dict, Any
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Security
security = HTTPBearer()

# Global variables for models (will be loaded on startup)
document_processor = None
fraud_detector = None
embedding_model = None
text_classifier = None
question_answering_model = None
document_qa_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize AI models on startup"""
    global document_processor, fraud_detector, embedding_model, text_classifier, question_answering_model, document_qa_service
    
    logger.info("Starting FraudDocAI AI Service...")
    
    try:
        # Initialize models with real Hugging Face models
        logger.info("Loading AI models...")
        
        # Import transformers
        from transformers import (
            pipeline, 
            AutoTokenizer, 
            AutoModelForSequenceClassification,
            AutoModelForQuestionAnswering,
            AutoModel
        )
        from sentence_transformers import SentenceTransformer
        
        # 1. Text Classification for fraud detection
        logger.info("Loading fraud detection classifier...")
        text_classifier = pipeline(
            "text-classification",
            model="cardiffnlp/twitter-roberta-base-emotion",  # Lighter, more appropriate model
            return_all_scores=True
        )
        
        # 2. Document Question Answering
        logger.info("Loading question answering model...")
        question_answering_model = pipeline(
            "question-answering",
            model="distilbert-base-uncased-distilled-squad"  # Lighter version
        )
        
        # 3. Sentence Embeddings for similarity search
        logger.info("Loading sentence transformer...")
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 4. Document processor (OCR + text extraction)
        logger.info("Initializing document processor...")
        document_processor = "ready"  # We'll implement OCR functionality
        
        # 5. Fraud detector (combination of models)
        logger.info("Initializing fraud detector...")
        fraud_detector = "ready"
        
        # 6. Document Question Answering Service
        logger.info("Initializing Document QA service...")
        from document_qa_service import DocumentQuestionAnsweringService
        document_qa_service = DocumentQuestionAnsweringService()
        
        logger.info("✅ All AI models loaded successfully!")
        logger.info(f"Models loaded: {len([m for m in [text_classifier, question_answering_model, embedding_model, document_qa_service] if m is not None])}/4")
        
    except Exception as e:
        logger.error(f"Failed to start AI Service: {e}")
        # Don't raise - start with basic functionality
        logger.warning("Starting with limited AI functionality...")
        document_processor = "limited"
        fraud_detector = "limited"
        embedding_model = "limited"
        text_classifier = "limited"
        question_answering_model = "limited"
        document_qa_service = "limited"

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
            "document_processor": document_processor is not None,
            "fraud_detector": fraud_detector is not None,
            "embedding_model": embedding_model is not None,
            "text_classifier": text_classifier is not None,
            "question_answering": question_answering_model is not None,
            "document_qa_service": document_qa_service is not None
        },
        "model_details": {
            "text_classifier": str(type(text_classifier).__name__) if text_classifier else "Not loaded",
            "question_answering": str(type(question_answering_model).__name__) if question_answering_model else "Not loaded",
            "embedding_model": str(type(embedding_model).__name__) if embedding_model else "Not loaded",
            "document_qa_service": str(type(document_qa_service).__name__) if document_qa_service else "Not loaded"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/process-document")
async def process_document(
    file: UploadFile = File(...),
    token: str = Depends(security)
):
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
        
        # Analyze text for fraud patterns using AI models
        fraud_analysis = await analyze_text_for_fraud(extracted_text)
        
        result = {
            "document_id": f"doc-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "filename": file.filename,
            "file_type": file.content_type,
            "file_size": len(content),
            "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            "fraud_score": fraud_analysis["fraud_score"],
            "fraud_risk_level": fraud_analysis["risk_level"],
            "detected_patterns": fraud_analysis["patterns"],
            "processing_time_ms": fraud_analysis["processing_time"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Document processed successfully: {file.filename}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-text")
async def analyze_text(
    text: str,
    token: str = Depends(security)
):
    """
    Analyze text for fraud patterns
    """
    try:
        logger.info("Analyzing text for fraud patterns")
        
        # Use real AI analysis
        fraud_analysis = await analyze_text_for_fraud(text)
        
        # Create detailed emotion analysis response
        emotions = []
        fraud_indicators = []
        
        # Extract emotion data from the classification result
        if text_classifier and text_classifier != "limited":
            try:
                classification_result = text_classifier(text[:512])
                if classification_result and len(classification_result) > 0:
                    for result in classification_result[0]:
                        emotions.append({
                            "emotion": result["label"],
                            "confidence": result["score"]
                        })
                        
                        # Check for fraud indicators based on emotions
                        if any(word in result["label"].lower() for word in ["anger", "fear", "sadness"]):
                            fraud_indicators.append({
                                "emotion": result["label"],
                                "confidence": result["score"],
                                "reason": f"Suspicious emotional tone detected: {result['label']}"
                            })
            except Exception as e:
                logger.warning(f"Emotion analysis failed: {e}")
        
        # Create emotion analysis object
        emotion_analysis = {
            "emotions": emotions,
            "fraud_indicators": fraud_indicators,
            "emotion_fraud_score": sum([indicator["confidence"] for indicator in fraud_indicators]),
            "model_used": "cardiffnlp/twitter-roberta-base-emotion",
            "text_analyzed": len(text),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Create pattern analysis object
        pattern_analysis = {
            "patterns": fraud_analysis["patterns"],
            "pattern_fraud_score": fraud_analysis["fraud_score"]
        }
        
        result = {
            "text_length": len(text),
            "fraud_score": fraud_analysis["fraud_score"],
            "fraud_risk_level": fraud_analysis["risk_level"],
            "detected_patterns": fraud_analysis["patterns"],
            "analysis_time_ms": fraud_analysis["processing_time"],
            "emotion_analysis": emotion_analysis,
            "pattern_analysis": pattern_analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-embeddings")
async def generate_embeddings(
    texts: List[str],
    token: str = Depends(security)
):
    """
    Generate embeddings for text documents
    """
    try:
        logger.info(f"Generating embeddings for {len(texts)} texts")
        
        # Generate real embeddings using sentence transformers
        embeddings = []
        start_time = datetime.utcnow()
        
        if embedding_model and hasattr(embedding_model, 'encode'):
            try:
                # Generate embeddings for all texts
                text_embeddings = embedding_model.encode(texts)
                
                for i, (text, embedding) in enumerate(zip(texts, text_embeddings)):
                    embeddings.append({
                        "text_index": i,
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "embedding": embedding.tolist(),
                        "embedding_dimension": len(embedding)
                    })
                
                generation_time = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                result = {
                    "embeddings": embeddings,
                    "model_used": "sentence-transformers/all-MiniLM-L6-v2",
                    "generation_time_ms": round(generation_time, 2),
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                logger.error(f"Error generating embeddings: {e}")
                # Fallback to mock embeddings
                embeddings = []
                for i, text in enumerate(texts):
                    embedding = [0.1] * 384
                    embeddings.append({
                        "text_index": i,
                        "text": text[:100] + "..." if len(text) > 100 else text,
                        "embedding": embedding,
                        "embedding_dimension": 384
                    })
                
                result = {
                    "embeddings": embeddings,
                    "model_used": "fallback-mock",
                    "generation_time_ms": 0,
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": "Model not available, using fallback"
                }
        else:
            # Fallback when model not loaded
            embeddings = []
            for i, text in enumerate(texts):
                embedding = [0.1] * 384
                embeddings.append({
                    "text_index": i,
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "embedding": embedding,
                    "embedding_dimension": 384
                })
            
            result = {
                "embeddings": embeddings,
                "model_used": "fallback-mock",
                "generation_time_ms": 0,
                "timestamp": datetime.utcnow().isoformat(),
                "error": "Embedding model not loaded"
            }
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fraud-patterns")
async def get_fraud_patterns(token: str = Depends(security)):
    """
    Get available fraud detection patterns
    """
    try:
        # TODO: Load from database
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

@app.post("/ask-document")
async def ask_document(
    question: str = Form(...),
    document_text: str = Form(...),
    token: str = Depends(security)
):
    """
    Ask a question about a document using Document Question Answering
    """
    try:
        logger.info(f"Processing document question: {question[:50]}...")
        
        if not document_qa_service or document_qa_service == "limited":
            raise HTTPException(
                status_code=503,
                detail="Document QA service not available"
            )
        
        # Use the Document QA service to answer the question
        result = document_qa_service.answer_question(question, document_text)
        
        return {
            "question": question,
            "answer": result["answer"],
            "confidence": result["confidence"],
            "start_position": result.get("start_position", 0),
            "end_position": result.get("end_position", 0),
            "context_used": result.get("context_used", ""),
            "model_used": result.get("model_used", "unknown"),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing document question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-document-fraud")
async def analyze_document_fraud(
    document_text: str = Form(...),
    token: str = Depends(security)
):
    """
    Analyze a document for fraud using predefined questions
    """
    try:
        logger.info("Analyzing document for fraud using QA...")
        
        if not document_qa_service or document_qa_service == "limited":
            raise HTTPException(
                status_code=503,
                detail="Document QA service not available"
            )
        
        # Use the Document QA service for fraud analysis
        result = document_qa_service.analyze_document_for_fraud_questions(document_text)
        
        return {
            "document_length": len(document_text),
            "fraud_analysis": result["fraud_analysis"],
            "overall_risk": result["overall_risk"],
            "total_risk_score": result["total_risk_score"],
            "questions_analyzed": result["questions_analyzed"],
            "model_used": result["model_used"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing document for fraud: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/qa-model-info")
async def get_qa_model_info(token: str = Depends(security)):
    """
    Get information about the Document QA model
    """
    try:
        if not document_qa_service or document_qa_service == "limited":
            return {
                "model_available": False,
                "error": "Document QA service not available"
            }
        
        model_info = document_qa_service.get_model_info()
        return {
            "model_available": True,
            "model_info": model_info,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting QA model info: {e}")
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

async def analyze_text_for_fraud(text: str) -> dict:
    """Analyze text for fraud patterns using AI models"""
    start_time = datetime.utcnow()
    
    try:
        # Initialize fraud patterns
        patterns = []
        fraud_score = 0.0
        
        # Check if models are loaded
        if text_classifier and text_classifier != "limited":
            # 1. Text classification for suspicious content
            try:
                classification_result = text_classifier(text[:512])  # Limit text length
                if classification_result and len(classification_result) > 0:
                    # Look for suspicious classifications (emotion model can detect stress/urgency)
                    for result in classification_result[0]:
                        if any(word in result["label"].lower() for word in ["anger", "fear", "sadness"]):
                            patterns.append({
                                "pattern": "suspicious_emotion",
                                "confidence": result["score"],
                                "description": f"Suspicious emotional tone detected: {result['label']}"
                            })
                            fraud_score += result["score"] * 0.2
            except Exception as e:
                logger.warning(f"Text classification failed: {e}")
        
        # 2. Pattern-based fraud detection
        fraud_keywords = [
            "urgent", "immediate", "confidential", "wire transfer", "bitcoin",
            "cryptocurrency", "offshore", "tax haven", "shell company",
            "forged", "fake", "duplicate", "altered", "tampered"
        ]
        
        text_lower = text.lower()
        for keyword in fraud_keywords:
            if keyword in text_lower:
                patterns.append({
                    "pattern": "fraud_keyword",
                    "confidence": 0.7,
                    "description": f"Fraud-related keyword detected: '{keyword}'"
                })
                fraud_score += 0.1
        
        # 3. Amount pattern detection
        import re
        amount_patterns = re.findall(r'\$[\d,]+\.?\d*', text)
        if len(amount_patterns) > 5:  # Many amounts might indicate suspicious activity
            patterns.append({
                "pattern": "excessive_amounts",
                "confidence": 0.6,
                "description": f"Excessive number of monetary amounts detected: {len(amount_patterns)}"
            })
            fraud_score += 0.2
        
        # 4. Email/phone pattern detection
        email_patterns = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if len(email_patterns) > 3:
            patterns.append({
                "pattern": "multiple_emails",
                "confidence": 0.5,
                "description": f"Multiple email addresses detected: {len(email_patterns)}"
            })
            fraud_score += 0.1
        
        # Normalize fraud score
        fraud_score = min(fraud_score, 1.0)
        
        # Determine risk level
        if fraud_score >= 0.8:
            risk_level = "critical"
        elif fraud_score >= 0.6:
            risk_level = "high"
        elif fraud_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return {
            "fraud_score": round(fraud_score, 3),
            "risk_level": risk_level,
            "patterns": patterns,
            "processing_time": round(processing_time, 2)
        }
        
    except Exception as e:
        logger.error(f"Error in fraud analysis: {e}")
        return {
            "fraud_score": 0.0,
            "risk_level": "low",
            "patterns": [],
            "processing_time": 0
        }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
