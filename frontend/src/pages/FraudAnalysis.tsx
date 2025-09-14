import React from 'react';
import { Shield, AlertTriangle, CheckCircle, FileText } from 'lucide-react';

const FraudAnalysis: React.FC = () => {
  // Mock data for fraud analysis
  const fraudPatterns = [
    {
      id: 'signature_forgery',
      name: 'Signature Forgery',
      description: 'Detects potentially forged signatures on documents',
      severity: 'high',
      confidence: 0.85,
      count: 12
    },
    {
      id: 'amount_tampering',
      name: 'Amount Tampering',
      description: 'Detects altered monetary amounts in documents',
      severity: 'critical',
      confidence: 0.92,
      count: 8
    },
    {
      id: 'duplicate_invoice',
      name: 'Duplicate Invoice',
      description: 'Identifies duplicate or near-duplicate invoices',
      severity: 'medium',
      confidence: 0.78,
      count: 15
    }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
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
        <h1 className="text-3xl font-bold text-gray-900">Fraud Analysis</h1>
        <p className="text-gray-600 mt-2">Monitor and analyze fraud detection patterns</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="document-card">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <Shield className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Alerts</p>
              <p className="text-2xl font-bold text-gray-900">35</p>
            </div>
          </div>
        </div>

        <div className="document-card">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">High Risk</p>
              <p className="text-2xl font-bold text-gray-900">8</p>
            </div>
          </div>
        </div>

        <div className="document-card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Resolved</p>
              <p className="text-2xl font-bold text-gray-900">27</p>
            </div>
          </div>
        </div>
      </div>

      {/* Fraud Patterns */}
      <div className="document-card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Detected Fraud Patterns</h2>
        <div className="space-y-4">
          {fraudPatterns.map((pattern) => (
            <div key={pattern.id} className="p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-gray-400" />
                  <h3 className="font-medium text-gray-900">{pattern.name}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(pattern.severity)}`}>
                    {pattern.severity.toUpperCase()}
                  </span>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">{pattern.count} detections</p>
                  <p className="text-xs text-gray-500">{(pattern.confidence * 100).toFixed(1)}% confidence</p>
                </div>
              </div>
              <p className="text-sm text-gray-600">{pattern.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Alerts */}
      <div className="document-card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Alerts</h2>
        <div className="space-y-3">
          {[
            {
              id: '1',
              document: 'invoice_001.pdf',
              pattern: 'Signature Forgery',
              severity: 'high',
              timestamp: '2024-01-15T10:30:00Z',
              status: 'pending'
            },
            {
              id: '2',
              document: 'loan_app_002.pdf',
              pattern: 'Amount Tampering',
              severity: 'critical',
              timestamp: '2024-01-15T09:15:00Z',
              status: 'investigating'
            },
            {
              id: '3',
              document: 'receipt_003.pdf',
              pattern: 'Duplicate Invoice',
              severity: 'medium',
              timestamp: '2024-01-15T08:45:00Z',
              status: 'resolved'
            }
          ].map((alert) => (
            <div key={alert.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-4">
                <div className={`p-1 rounded-full ${getSeverityColor(alert.severity)}`}>
                  <AlertTriangle className="h-4 w-4" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">{alert.document}</p>
                  <p className="text-sm text-gray-500">{alert.pattern}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-900">{new Date(alert.timestamp).toLocaleDateString()}</p>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  alert.status === 'resolved' ? 'text-green-600 bg-green-100' :
                  alert.status === 'investigating' ? 'text-yellow-600 bg-yellow-100' :
                  'text-red-600 bg-red-100'
                }`}>
                  {alert.status.toUpperCase()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FraudAnalysis;
