"""
FraudDocAI - Emotion-Based Fraud Detection
Uses cardiffnlp/twitter-roberta-base-emotion model for fraud analysis
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from transformers import pipeline
import re

logger = logging.getLogger(__name__)

class EmotionFraudDetector:
    """Fraud detector using emotion analysis from Hugging Face models"""
    
    def __init__(self):
        self.emotion_model = None
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the emotion classification model"""
        try:
            logger.info("Loading cardiffnlp/twitter-roberta-base-emotion model...")
            self.emotion_model = pipeline(
                "text-classification",
                model="cardiffnlp/twitter-roberta-base-emotion",
                return_all_scores=True
            )
            self.model_loaded = True
            logger.info("✅ Emotion model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load emotion model: {e}")
            self.model_loaded = False
    
    def analyze_emotions(self, text: str) -> Dict[str, Any]:
        """Analyze text for emotional patterns that might indicate fraud"""
        if not self.model_loaded or not self.emotion_model:
            return {
                "emotions": [],
                "fraud_indicators": [],
                "emotion_fraud_score": 0.0,
                "error": "Model not loaded"
            }
        
        try:
            # Limit text length for model processing
            text_sample = text[:512] if len(text) > 512 else text
            
            # Get emotion predictions
            emotion_results = self.emotion_model(text_sample)
            
            # Process emotion results
            emotions = []
            fraud_indicators = []
            emotion_fraud_score = 0.0
            
            if emotion_results and len(emotion_results) > 0:
                for result in emotion_results[0]:
                    emotion_data = {
                        "emotion": result["label"],
                        "confidence": round(result["score"], 3)
                    }
                    emotions.append(emotion_data)
                    
                    # Check for fraud-indicating emotions
                    if self._is_fraud_indicating_emotion(result["label"], result["score"]):
                        fraud_indicators.append({
                            "emotion": result["label"],
                            "confidence": round(result["score"], 3),
                            "reason": self._get_fraud_reason(result["label"])
                        })
                        emotion_fraud_score += result["score"] * self._get_emotion_weight(result["label"])
            
            # Normalize score
            emotion_fraud_score = min(emotion_fraud_score, 1.0)
            
            return {
                "emotions": emotions,
                "fraud_indicators": fraud_indicators,
                "emotion_fraud_score": round(emotion_fraud_score, 3),
                "model_used": "cardiffnlp/twitter-roberta-base-emotion",
                "text_analyzed": len(text_sample),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in emotion analysis: {e}")
            return {
                "emotions": [],
                "fraud_indicators": [],
                "emotion_fraud_score": 0.0,
                "error": str(e)
            }
    
    def _is_fraud_indicating_emotion(self, emotion: str, confidence: float) -> bool:
        """Check if an emotion indicates potential fraud"""
        fraud_emotions = ["anger", "fear", "sadness"]
        return emotion.lower() in fraud_emotions and confidence > 0.3
    
    def _get_fraud_reason(self, emotion: str) -> str:
        """Get explanation for why an emotion indicates fraud"""
        reasons = {
            "anger": "Anger can indicate frustration with legitimate processes, suggesting potential fraud",
            "fear": "Fear often accompanies fraudulent activities due to risk of discovery",
            "sadness": "Sadness might indicate desperation leading to fraudulent behavior"
        }
        return reasons.get(emotion.lower(), "Emotional pattern may indicate suspicious activity")
    
    def _get_emotion_weight(self, emotion: str) -> float:
        """Get weight for emotion in fraud scoring"""
        weights = {
            "anger": 0.4,
            "fear": 0.6,
            "sadness": 0.3
        }
        return weights.get(emotion.lower(), 0.2)
    
    def analyze_fraud_patterns(self, text: str) -> Dict[str, Any]:
        """Complete fraud analysis combining emotion and pattern detection"""
        start_time = datetime.utcnow()
        
        # Get emotion analysis
        emotion_analysis = self.analyze_emotions(text)
        
        # Traditional pattern-based analysis
        pattern_analysis = self._analyze_patterns(text)
        
        # Combine results
        total_fraud_score = (
            emotion_analysis["emotion_fraud_score"] * 0.4 +  # 40% emotion
            pattern_analysis["pattern_fraud_score"] * 0.6    # 60% patterns
        )
        
        # Determine risk level
        if total_fraud_score >= 0.8:
            risk_level = "critical"
        elif total_fraud_score >= 0.6:
            risk_level = "high"
        elif total_fraud_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return {
            "fraud_score": round(total_fraud_score, 3),
            "risk_level": risk_level,
            "emotion_analysis": emotion_analysis,
            "pattern_analysis": pattern_analysis,
            "processing_time_ms": round(processing_time, 2),
            "model_used": "cardiffnlp/twitter-roberta-base-emotion + pattern-matching",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _analyze_patterns(self, text: str) -> Dict[str, Any]:
        """Traditional pattern-based fraud detection"""
        patterns = []
        pattern_fraud_score = 0.0
        
        # Fraud keywords
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
                pattern_fraud_score += 0.1
        
        # Amount patterns
        amount_patterns = re.findall(r'\$[\d,]+\.?\d*', text)
        if len(amount_patterns) > 5:
            patterns.append({
                "pattern": "excessive_amounts",
                "confidence": 0.6,
                "description": f"Excessive number of monetary amounts: {len(amount_patterns)}"
            })
            pattern_fraud_score += 0.2
        
        # Urgency indicators
        urgency_words = ["urgent", "immediate", "asap", "rush", "emergency", "critical"]
        urgency_count = sum(1 for word in urgency_words if word in text_lower)
        if urgency_count > 2:
            patterns.append({
                "pattern": "urgency_indicators",
                "confidence": 0.6,
                "description": f"Multiple urgency indicators: {urgency_count}"
            })
            pattern_fraud_score += 0.15
        
        return {
            "patterns": patterns,
            "pattern_fraud_score": min(pattern_fraud_score, 1.0)
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "model_name": "cardiffnlp/twitter-roberta-base-emotion",
            "model_loaded": self.model_loaded,
            "model_type": "text-classification",
            "purpose": "emotion-based fraud detection",
            "supported_emotions": ["anger", "fear", "joy", "love", "sadness", "surprise"],
            "fraud_indicating_emotions": ["anger", "fear", "sadness"]
        }

# Test function
def test_emotion_detector():
    """Test the emotion fraud detector with sample texts"""
    detector = EmotionFraudDetector()
    
    # Test with high-risk text
    high_risk_text = "URGENT: Please wire transfer $50,000 immediately! This is confidential and must be done ASAP!"
    
    print("Testing Emotion Fraud Detector")
    print("=" * 50)
    print(f"Model Info: {detector.get_model_info()}")
    print("\nHigh Risk Text Analysis:")
    print(f"Text: {high_risk_text}")
    
    result = detector.analyze_fraud_patterns(high_risk_text)
    print(f"\nFraud Score: {result['fraud_score']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Emotion Analysis: {result['emotion_analysis']}")
    print(f"Pattern Analysis: {result['pattern_analysis']}")

if __name__ == "__main__":
    test_emotion_detector()
