import React, { useState, useEffect } from 'react';
import { api, Document, DocumentQAResponse, DocumentFraudAnalysisResponse } from '../services/api';
import toast from 'react-hot-toast';

interface QAResult {
  question: string;
  answer: string;
  confidence: number;
  timestamp: string;
}

interface FraudAnalysisResult {
  overall_risk: string;
  total_risk_score: number;
  fraud_analysis: Array<{
    question: string;
    answer: string;
    confidence: number;
    category: string;
    fraud_indicators: {
      risk_score: number;
      indicators: string[];
    };
    risk_score: number;
  }>;
}

const DocumentQA: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);
  const [question, setQuestion] = useState('');
  const [qaResults, setQAResults] = useState<QAResult[]>([]);
  const [fraudAnalysis, setFraudAnalysis] = useState<FraudAnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Load documents on component mount
  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await api.getDocuments();
      setDocuments(response.documents);
    } catch (error) {
      console.error('Failed to load documents:', error);
      toast.error('Failed to load documents');
    }
  };

  const askQuestion = async () => {
    if (!selectedDocument || !question.trim()) {
      toast.error('Please select a document and enter a question');
      return;
    }

    if (!selectedDocument.extracted_text) {
      toast.error('No text available for this document');
      return;
    }

    setIsLoading(true);
    try {
      const response: DocumentQAResponse = await api.askDocument({
        question: question.trim(),
        document_text: selectedDocument.extracted_text
      });

      const newResult: QAResult = {
        question: response.question,
        answer: response.answer,
        confidence: response.confidence,
        timestamp: response.timestamp
      };

      setQAResults(prev => [newResult, ...prev]);
      setQuestion('');
      toast.success('Question answered successfully!');
    } catch (error) {
      console.error('Failed to ask question:', error);
      toast.error('Failed to get answer');
    } finally {
      setIsLoading(false);
    }
  };

  const analyzeDocumentFraud = async () => {
    if (!selectedDocument || !selectedDocument.extracted_text) {
      toast.error('Please select a document with extracted text');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response: DocumentFraudAnalysisResponse = await api.analyzeDocumentFraud({
        document_text: selectedDocument.extracted_text
      });

      setFraudAnalysis({
        overall_risk: response.overall_risk,
        total_risk_score: response.total_risk_score,
        fraud_analysis: response.fraud_analysis
      });

      toast.success('Fraud analysis completed!');
    } catch (error) {
      console.error('Failed to analyze document:', error);
      toast.error('Failed to analyze document for fraud');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Document Question & Answering</h1>
        <p className="text-gray-600">Ask questions about your uploaded documents and get AI-powered answers</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Document Selection */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Select Document</h2>
            
            {documents.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No documents uploaded yet</p>
            ) : (
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {documents.map((doc) => (
                  <div
                    key={doc.id}
                    onClick={() => setSelectedDocument(doc)}
                    className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                      selectedDocument?.id === doc.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-medium text-gray-900">{doc.original_filename}</h3>
                        <p className="text-sm text-gray-500">
                          {doc.fraud_risk_level && (
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(doc.fraud_risk_level)}`}>
                              {doc.fraud_risk_level.toUpperCase()}
                            </span>
                          )}
                        </p>
                      </div>
                      <div className="text-right text-sm text-gray-500">
                        <p>{(doc.file_size / 1024).toFixed(1)} KB</p>
                        <p>{doc.status}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Question Input */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Ask a Question</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Question about the selected document
                </label>
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="e.g., What is the total amount mentioned? Who is the sender? What is the purpose of this transaction?"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows={3}
                />
              </div>
              
              <button
                onClick={askQuestion}
                disabled={!selectedDocument || !question.trim() || isLoading}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Asking...' : 'Ask Question'}
              </button>
            </div>
          </div>

          {/* Fraud Analysis Button */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Fraud Analysis</h2>
            <p className="text-gray-600 mb-4">
              Get a comprehensive fraud analysis using AI-powered questions
            </p>
            
            <button
              onClick={analyzeDocumentFraud}
              disabled={!selectedDocument || !selectedDocument.extracted_text || isAnalyzing}
              className="w-full bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {isAnalyzing ? 'Analyzing...' : 'Analyze for Fraud'}
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="space-y-6">
          {/* Q&A Results */}
          {qaResults.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Question & Answer History</h2>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {qaResults.map((result, index) => (
                  <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-medium text-gray-900">{result.question}</h3>
                      <span className={`text-sm font-medium ${getConfidenceColor(result.confidence)}`}>
                        {Math.round(result.confidence * 100)}% confidence
                      </span>
                    </div>
                    <p className="text-gray-700 mb-2">{result.answer}</p>
                    <p className="text-xs text-gray-500">
                      {new Date(result.timestamp).toLocaleString()}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Fraud Analysis Results */}
          {fraudAnalysis && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Fraud Analysis Results</h2>
              
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium">Overall Risk:</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(fraudAnalysis.overall_risk)}`}>
                    {fraudAnalysis.overall_risk.toUpperCase()}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="font-medium">Risk Score:</span>
                  <span className="text-lg font-bold">{Math.round(fraudAnalysis.total_risk_score * 100)}%</span>
                </div>
              </div>

              <div className="space-y-3 max-h-96 overflow-y-auto">
                {fraudAnalysis.fraud_analysis.map((item, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-medium text-gray-900">{item.question}</h3>
                      <div className="text-right text-sm">
                        <span className={`font-medium ${getConfidenceColor(item.confidence)}`}>
                          {Math.round(item.confidence * 100)}% confidence
                        </span>
                        <br />
                        <span className="text-gray-500">Risk: {Math.round(item.risk_score * 100)}%</span>
                      </div>
                    </div>
                    
                    <p className="text-gray-700 mb-2">{item.answer}</p>
                    
                    {item.fraud_indicators.indicators.length > 0 && (
                      <div className="mt-2">
                        <p className="text-sm font-medium text-red-600 mb-1">Fraud Indicators:</p>
                        <ul className="text-sm text-red-600 list-disc list-inside">
                          {item.fraud_indicators.indicators.map((indicator, idx) => (
                            <li key={idx}>{indicator}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentQA;
