const API_BASE_URL = 'http://localhost:8080/api/v1';

export interface UploadResponse {
  message: string;
  file_id: string;
  file_name: string;
  file_size: number;
  file_url: string;
  status: string;
}

export interface Emotion {
  emotion: string;
  confidence: number;
}

export interface FraudIndicator {
  emotion: string;
  confidence: number;
  reason: string;
}

export interface EmotionAnalysis {
  emotions: Emotion[];
  fraud_indicators: FraudIndicator[];
  emotion_fraud_score: number;
  model_used: string;
  text_analyzed: number;
  timestamp: string;
}

export interface Pattern {
  pattern: string;
  confidence: number;
  description: string;
}

export interface PatternAnalysis {
  patterns: Pattern[];
  pattern_fraud_score: number;
}

export interface Document {
  id: string;
  user_id: string | null;
  filename: string;
  original_filename: string;
  file_path: string;
  file_size: number;
  mime_type: string;
  document_type: string | null;
  status: string;
  fraud_score: number | null;
  fraud_risk_level: string;
  extracted_text: string | null;
  emotion_analysis?: EmotionAnalysis;
  pattern_analysis?: PatternAnalysis;
  metadata: any;
  created_at: string;
  updated_at: string;
}

export interface DocumentsResponse {
  documents: Document[];
  total: number;
  status: string;
}

export interface FraudAnalysisResponse {
  fraud_score: number;
  risk_level: string;
  patterns: string[];
  confidence: number;
  status: string;
}

export const api = {
  // Upload document to backend
  async uploadDocument(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  },

  // Analyze document for fraud
  async analyzeDocument(fileId: string): Promise<FraudAnalysisResponse> {
    const response = await fetch(`${API_BASE_URL}/fraud/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ file_id: fileId }),
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }

    return response.json();
  },

  // Get all documents
  async getDocuments(): Promise<DocumentsResponse> {
    const response = await fetch(`${API_BASE_URL}/documents/`);
    
    if (!response.ok) {
      throw new Error(`Failed to get documents: ${response.statusText}`);
    }

    return response.json();
  },

  // Get document details
  async getDocument(fileId: string) {
    const response = await fetch(`${API_BASE_URL}/documents/${fileId}`);
    
    if (!response.ok) {
      throw new Error(`Failed to get document: ${response.statusText}`);
    }

    return response.json();
  }
};
