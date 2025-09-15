"""
FraudDocAI - Document Question Answering Service
Uses Hugging Face models for intelligent document querying
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from transformers import pipeline
import re

logger = logging.getLogger(__name__)

class DocumentQuestionAnsweringService:
    """Document Question Answering service for fraud detection queries"""
    
    def __init__(self):
        self.qa_model = None
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the question answering model"""
        try:
            logger.info("Loading distilbert-base-uncased-distilled-squad model...")
            self.qa_model = pipeline(
                "question-answering",
                model="distilbert-base-uncased-distilled-squad"
            )
            self.model_loaded = True
            logger.info("✅ Document QA model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load QA model: {e}")
            self.model_loaded = False
    
    def answer_question(self, question: str, context: str) -> Dict[str, Any]:
        """Answer a question about a document context"""
        if not self.model_loaded or not self.qa_model:
            return {
                "answer": "Model not available",
                "confidence": 0.0,
                "error": "QA model not loaded"
            }
        
        try:
            # Limit context length for model processing
            max_context_length = 512
            if len(context) > max_context_length:
                # Try to find the most relevant part of the context
                context = self._extract_relevant_context(question, context, max_context_length)
            
            # Get answer from the model
            result = self.qa_model(question=question, context=context)
            
            return {
                "answer": result["answer"],
                "confidence": round(result["score"], 3),
                "start_position": result["start"],
                "end_position": result["end"],
                "context_used": context[:200] + "..." if len(context) > 200 else context,
                "model_used": "distilbert-base-uncased-distilled-squad",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in question answering: {e}")
            return {
                "answer": "Error processing question",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _extract_relevant_context(self, question: str, context: str, max_length: int) -> str:
        """Extract the most relevant part of the context for the question"""
        try:
            # Simple keyword-based context extraction
            question_words = set(question.lower().split())
            context_sentences = context.split('.')
            
            # Score sentences based on keyword overlap
            scored_sentences = []
            for sentence in context_sentences:
                sentence_words = set(sentence.lower().split())
                overlap = len(question_words.intersection(sentence_words))
                scored_sentences.append((overlap, sentence))
            
            # Sort by relevance and take the most relevant sentences
            scored_sentences.sort(reverse=True)
            
            relevant_context = ""
            for _, sentence in scored_sentences:
                if len(relevant_context + sentence) <= max_length:
                    relevant_context += sentence + ". "
                else:
                    break
            
            return relevant_context.strip() or context[:max_length]
            
        except Exception as e:
            logger.warning(f"Error extracting relevant context: {e}")
            return context[:max_length]
    
    def analyze_document_for_fraud_questions(self, document_text: str) -> Dict[str, Any]:
        """Analyze document using predefined fraud detection questions"""
        if not self.model_loaded:
            return {
                "fraud_analysis": [],
                "overall_risk": "unknown",
                "error": "QA model not loaded"
            }
        
        # Predefined fraud detection questions
        fraud_questions = [
            {
                "question": "What is the total amount mentioned in this document?",
                "category": "amount_verification",
                "risk_weight": 0.3
            },
            {
                "question": "Are there any urgent or immediate payment requests?",
                "category": "urgency_indicators",
                "risk_weight": 0.4
            },
            {
                "question": "What contact information is provided in this document?",
                "category": "contact_verification",
                "risk_weight": 0.2
            },
            {
                "question": "Are there any mentions of wire transfers or cryptocurrency?",
                "category": "payment_methods",
                "risk_weight": 0.5
            },
            {
                "question": "What is the purpose or reason for this transaction?",
                "category": "transaction_purpose",
                "risk_weight": 0.3
            },
            {
                "question": "Are there any confidentiality or secrecy requirements mentioned?",
                "category": "secrecy_indicators",
                "risk_weight": 0.6
            }
        ]
        
        fraud_analysis = []
        total_risk_score = 0.0
        
        for qa_item in fraud_questions:
            try:
                result = self.answer_question(qa_item["question"], document_text)
                
                # Analyze the answer for fraud indicators
                fraud_indicators = self._analyze_answer_for_fraud(
                    qa_item["question"], 
                    result["answer"], 
                    qa_item["category"]
                )
                
                analysis_item = {
                    "question": qa_item["question"],
                    "answer": result["answer"],
                    "confidence": result["confidence"],
                    "category": qa_item["category"],
                    "fraud_indicators": fraud_indicators,
                    "risk_score": fraud_indicators["risk_score"] * qa_item["risk_weight"]
                }
                
                fraud_analysis.append(analysis_item)
                total_risk_score += analysis_item["risk_score"]
                
            except Exception as e:
                logger.error(f"Error analyzing question '{qa_item['question']}': {e}")
                fraud_analysis.append({
                    "question": qa_item["question"],
                    "answer": "Error processing question",
                    "confidence": 0.0,
                    "category": qa_item["category"],
                    "fraud_indicators": {"risk_score": 0.0, "indicators": []},
                    "risk_score": 0.0,
                    "error": str(e)
                })
        
        # Determine overall risk level
        if total_risk_score >= 0.7:
            overall_risk = "high"
        elif total_risk_score >= 0.4:
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        return {
            "fraud_analysis": fraud_analysis,
            "overall_risk": overall_risk,
            "total_risk_score": round(total_risk_score, 3),
            "questions_analyzed": len(fraud_questions),
            "model_used": "distilbert-base-uncased-distilled-squad",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _analyze_answer_for_fraud(self, question: str, answer: str, category: str) -> Dict[str, Any]:
        """Analyze an answer for fraud indicators"""
        fraud_indicators = []
        risk_score = 0.0
        
        answer_lower = answer.lower()
        
        # Category-specific fraud detection
        if category == "urgency_indicators":
            urgency_words = ["urgent", "immediate", "asap", "rush", "emergency", "critical", "now"]
            for word in urgency_words:
                if word in answer_lower:
                    fraud_indicators.append(f"Urgency indicator: '{word}'")
                    risk_score += 0.2
        
        elif category == "payment_methods":
            suspicious_payment_words = ["wire transfer", "bitcoin", "cryptocurrency", "cash", "untraceable"]
            for word in suspicious_payment_words:
                if word in answer_lower:
                    fraud_indicators.append(f"Suspicious payment method: '{word}'")
                    risk_score += 0.3
        
        elif category == "secrecy_indicators":
            secrecy_words = ["confidential", "secret", "private", "don't tell", "keep quiet", "discrete"]
            for word in secrecy_words:
                if word in answer_lower:
                    fraud_indicators.append(f"Secrecy indicator: '{word}'")
                    risk_score += 0.4
        
        elif category == "amount_verification":
            # Check for unusually large amounts
            amount_patterns = re.findall(r'\$[\d,]+\.?\d*', answer)
            for amount_str in amount_patterns:
                try:
                    amount = float(amount_str.replace('$', '').replace(',', ''))
                    if amount > 10000:  # Large amount threshold
                        fraud_indicators.append(f"Large amount detected: {amount_str}")
                        risk_score += 0.2
                except ValueError:
                    pass
        
        # General fraud indicators
        general_fraud_words = ["fake", "forged", "duplicate", "altered", "tampered", "offshore", "shell company"]
        for word in general_fraud_words:
            if word in answer_lower:
                fraud_indicators.append(f"General fraud indicator: '{word}'")
                risk_score += 0.3
        
        return {
            "risk_score": min(risk_score, 1.0),
            "indicators": fraud_indicators
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "model_name": "distilbert-base-uncased-distilled-squad",
            "model_loaded": self.model_loaded,
            "model_type": "question-answering",
            "purpose": "document question answering for fraud detection",
            "max_context_length": 512,
            "supported_languages": ["english"]
        }

# Test function
def test_document_qa():
    """Test the document QA service with sample data"""
    qa_service = DocumentQuestionAnsweringService()
    
    # Sample document text
    sample_document = """
    URGENT: Please wire transfer $50,000 immediately to account 1234567890. 
    This is a confidential transaction that must be completed ASAP. 
    Contact us at urgent@fakebank.com for verification. 
    The purpose is for offshore investment in cryptocurrency.
    """
    
    print("Testing Document Question Answering Service")
    print("=" * 50)
    print(f"Model Info: {qa_service.get_model_info()}")
    print(f"\nSample Document: {sample_document}")
    
    # Test individual question
    result = qa_service.answer_question("What is the total amount mentioned?", sample_document)
    print(f"\nIndividual Question Result: {result}")
    
    # Test fraud analysis
    fraud_result = qa_service.analyze_document_for_fraud_questions(sample_document)
    print(f"\nFraud Analysis Result: {fraud_result}")

if __name__ == "__main__":
    test_document_qa()
