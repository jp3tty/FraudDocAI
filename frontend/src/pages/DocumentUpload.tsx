import React, { useState, useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle, CheckCircle, Shield, TrendingUp } from 'lucide-react';
import toast from 'react-hot-toast';
import { api, UploadResponse, Document } from '../services/api';

interface UploadedFile {
  file: File;
  id: string;
  fileId?: string; // Backend file ID
  status: 'uploading' | 'processing' | 'completed' | 'error';
  fraudScore?: number | null;
  riskLevel?: string;
  error?: string;
  fileUrl?: string;
}

// Helper functions for OCR quality display
const getQualityBadgeClass = (qualityLevel: string): string => {
  switch (qualityLevel) {
    case 'excellent':
      return 'bg-green-100 text-green-800';
    case 'good':
      return 'bg-yellow-100 text-yellow-800';
    case 'fair':
      return 'bg-orange-100 text-orange-800';
    case 'poor':
      return 'bg-red-100 text-red-800';
    case 'failed':
      return 'bg-gray-100 text-gray-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const getQualityBarClass = (qualityLevel: string): string => {
  switch (qualityLevel) {
    case 'excellent':
      return 'bg-green-500';
    case 'good':
      return 'bg-yellow-500';
    case 'fair':
      return 'bg-orange-500';
    case 'poor':
      return 'bg-red-500';
    case 'failed':
      return 'bg-gray-500';
    default:
      return 'bg-gray-500';
  }
};

const DocumentUpload: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [documents, setDocuments] = useState<Document[]>([]);

  // Poll for document updates to get fraud analysis results
  useEffect(() => {
    const pollDocuments = async () => {
      try {
        const response = await api.getDocuments();
        setDocuments(response.documents);
        
        // Update uploaded files with fraud analysis results
        setUploadedFiles(prev => 
          prev.map(file => {
            const doc = response.documents.find(d => d.id === file.fileId);
            if (doc) {
              return {
                ...file,
                status: doc.status === 'processed' ? 'completed' : 'processing',
                fraudScore: doc.fraud_score,
                riskLevel: doc.fraud_risk_level
              };
            }
            return file;
          })
        );
      } catch (error) {
        console.error('Failed to fetch documents:', error);
      }
    };

    // Poll every 2 seconds if there are processing documents
    const hasProcessingFiles = uploadedFiles.some(f => f.status === 'processing');
    if (hasProcessingFiles) {
      const interval = setInterval(pollDocuments, 2000);
      return () => clearInterval(interval);
    }
  }, [uploadedFiles]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setIsUploading(true);
    
    for (const file of acceptedFiles) {
      const fileId = Math.random().toString(36).substr(2, 9);
      const newFile: UploadedFile = {
        file,
        id: fileId,
        status: 'uploading'
      };

      setUploadedFiles(prev => [...prev, newFile]);

      try {
        // Upload to backend
        const uploadResponse: UploadResponse = await api.uploadDocument(file);
        
        // Update with backend response
        setUploadedFiles(prev => 
          prev.map(f => 
            f.id === fileId 
              ? { 
                  ...f, 
                  status: 'processing',
                  fileId: uploadResponse.file_id,
                  fileUrl: uploadResponse.file_url
                }
              : f
          )
        );

        // Fraud analysis happens automatically in background
        // The polling mechanism will pick up the results
        
      } catch (error) {
        setUploadedFiles(prev => 
          prev.map(f => 
            f.id === fileId 
              ? { 
                  ...f, 
                  status: 'error', 
                  error: error instanceof Error ? error.message : 'Upload failed' 
                }
              : f
          )
        );
        toast.error(`Failed to upload ${file.name}`);
      }
    }
    
    setIsUploading(false);
  }, []);


  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/tiff': ['.tiff', '.tif'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: true
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'uploading':
        return <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>;
      case 'processing':
        return <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-yellow-600"></div>;
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-600" />;
      default:
        return null;
    }
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'high': return 'text-red-600 bg-red-100';
      case 'critical': return 'text-red-800 bg-red-200';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Document Upload</h1>
        <p className="text-gray-600 mt-2">Upload financial documents for fraud analysis</p>
      </div>

      {/* Upload Zone */}
      <div
        {...getRootProps()}
        className={`upload-zone ${isDragActive ? 'dragover' : ''} ${isUploading ? 'opacity-50 pointer-events-none' : ''}`}
      >
        <input {...getInputProps()} />
        <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        {isDragActive ? (
          <p className="text-lg text-blue-600">Drop the files here...</p>
        ) : (
          <div>
            <p className="text-lg text-gray-600 mb-2">
              Drag & drop files here, or click to select files
            </p>
            <p className="text-sm text-gray-500">
              Supports PDF, JPG, PNG, TIFF, DOCX, and TXT files
            </p>
          </div>
        )}
      </div>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="document-card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Uploaded Files</h2>
          <div className="space-y-3">
            {uploadedFiles.map((file) => (
              <div key={file.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-4">
                  <FileText className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="font-medium text-gray-900">{file.file.name}</p>
                    <p className="text-sm text-gray-500">
                      {(file.file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  {getStatusIcon(file.status)}
                  
                  {file.status === 'completed' && file.fraudScore !== undefined && file.fraudScore !== null && (
                    <>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelColor(file.riskLevel || 'low')}`}>
                        {file.riskLevel?.toUpperCase()}
                      </span>
                      <span className="text-sm font-medium text-gray-900">
                        {(file.fraudScore * 100).toFixed(1)}%
                      </span>
                    </>
                  )}
                  
                  {file.status === 'error' && (
                    <span className="text-sm text-red-600">{file.error}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Fraud Analysis Results */}
      {documents.length > 0 && (
        <div className="document-card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <Shield className="h-5 w-5 mr-2 text-blue-600" />
            Fraud Analysis Results
          </h2>
          <div className="space-y-4">
            {documents
              .filter(doc => doc.status === 'processed' && doc.fraud_score !== null)
              .map((doc) => (
                <div key={doc.id} className="border rounded-lg p-4 bg-white">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <FileText className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="font-medium text-gray-900">{doc.original_filename}</p>
                        <p className="text-sm text-gray-500">
                          Uploaded {new Date(doc.created_at).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskLevelColor(doc.fraud_risk_level)}`}>
                        {doc.fraud_risk_level?.toUpperCase()} RISK
                      </span>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-gray-900">
                          {(doc.fraud_score! * 100).toFixed(1)}%
                        </p>
                        <p className="text-xs text-gray-500">Fraud Score</p>
                      </div>
                    </div>
                  </div>
                  
                  {doc.extracted_text && (
                    <div className="mt-3">
                      <p className="text-sm font-medium text-gray-700 mb-2">Extracted Text:</p>
                      <div className="bg-gray-50 p-3 rounded text-sm text-gray-600 max-h-32 overflow-y-auto">
                        {doc.extracted_text}
                      </div>
                    </div>
                  )}

                  {/* OCR Quality Indicators */}
                  {doc.ocr_quality && (
                    <div className="mt-3 border-t pt-3">
                      <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                        <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                        OCR Quality Analysis
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div className="bg-blue-50 p-3 rounded">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-medium text-gray-600">Confidence Score</span>
                            <span className={`px-2 py-1 rounded text-xs font-bold ${getQualityBadgeClass(doc.ocr_quality.quality_level)}`}>
                              {doc.ocr_quality.confidence_score}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${getQualityBarClass(doc.ocr_quality.quality_level)}`}
                              style={{ width: `${Math.min(doc.ocr_quality.confidence_score, 100)}%` }}
                            ></div>
                          </div>
                        </div>
                        
                        <div className="bg-blue-50 p-3 rounded">
                          <div className="text-xs text-gray-600 mb-1">
                            <span className="font-medium">Quality Level:</span> {doc.ocr_quality.quality_level.toUpperCase()}
                          </div>
                          <div className="text-xs text-gray-600 mb-1">
                            <span className="font-medium">Text Blocks:</span> {doc.ocr_quality.text_blocks}
                          </div>
                          <div className="text-xs text-gray-600">
                            <span className="font-medium">Preprocessing:</span> {doc.ocr_quality.preprocessing_applied ? 'Applied' : 'Not needed'}
                          </div>
                        </div>
                      </div>
                      
                      <div className="mt-2 p-2 bg-gray-50 rounded text-xs text-gray-600">
                        <span className="font-medium">Processing Notes:</span> {doc.ocr_quality.processing_notes}
                      </div>
                    </div>
                  )}

                  {/* Emotion Analysis Results */}
                  {doc.emotion_analysis && (() => {
                    try {
                      const emotionData = typeof doc.emotion_analysis === 'string' 
                        ? JSON.parse(doc.emotion_analysis) 
                        : doc.emotion_analysis;
                      return (
                        <div className="mt-4 border-t pt-4">
                          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
                            <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                            Emotion Analysis (AI-Powered)
                          </h4>
                          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                            {emotionData.emotions?.map((emotion: any, index: number) => (
                          <div key={index} className="bg-purple-50 p-2 rounded text-xs">
                            <div className="flex justify-between items-center">
                              <span className="font-medium capitalize">{emotion.emotion}</span>
                              <span className="text-purple-600">{(emotion.confidence * 100).toFixed(1)}%</span>
                            </div>
                            <div className="w-full bg-purple-200 rounded-full h-1 mt-1">
                              <div 
                                className="bg-purple-500 h-1 rounded-full" 
                                style={{ width: `${emotion.confidence * 100}%` }}
                              ></div>
                            </div>
                          </div>
                        ))}
                      </div>
                          {emotionData.fraud_indicators?.length > 0 && (
                            <div className="mt-3">
                              <p className="text-xs font-medium text-red-600 mb-2">Fraud-Indicating Emotions:</p>
                              <div className="space-y-1">
                                {emotionData.fraud_indicators.map((indicator: any, index: number) => (
                                  <div key={index} className="text-xs text-red-600 bg-red-50 p-2 rounded">
                                    {indicator.emotion} ({(indicator.confidence * 100).toFixed(1)}%) - {indicator.reason}
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    } catch (error) {
                      console.error('Error parsing emotion analysis:', error);
                      return null;
                    }
                  })()}

                  {/* Pattern Analysis Results */}
                  {doc.pattern_analysis && (() => {
                    try {
                      const patternData = typeof doc.pattern_analysis === 'string' 
                        ? JSON.parse(doc.pattern_analysis) 
                        : doc.pattern_analysis;
                      return patternData.patterns?.length > 0 ? (
                        <div className="mt-4 border-t pt-4">
                          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
                            <span className="w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
                            Pattern Analysis
                          </h4>
                          <div className="space-y-2">
                            {patternData.patterns.map((pattern: any, index: number) => (
                          <div key={index} className="bg-orange-50 p-2 rounded text-xs">
                            <div className="flex justify-between items-center">
                              <span className="font-medium">{pattern.description}</span>
                              <span className="text-orange-600">{(pattern.confidence * 100).toFixed(1)}%</span>
                            </div>
                          </div>
                            ))}
                          </div>
                        </div>
                      ) : null;
                    } catch (error) {
                      console.error('Error parsing pattern analysis:', error);
                      return null;
                    }
                  })()}
                </div>
              ))}
            
            {documents.filter(doc => doc.status === 'processed' && doc.fraud_score !== null).length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <Shield className="h-12 w-12 mx-auto mb-3 text-gray-300" />
                <p>No fraud analysis results yet. Upload documents to see analysis.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="document-card">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Supported Document Types</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Financial Documents</h4>
            <ul className="space-y-1">
              <li>• Invoices and receipts</li>
              <li>• Bank statements</li>
              <li>• Loan applications</li>
              <li>• Insurance claims</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Fraud Detection</h4>
            <ul className="space-y-1">
              <li>• Signature verification</li>
              <li>• Amount tampering</li>
              <li>• Duplicate detection</li>
              <li>• Pattern analysis</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
