import React from 'react';
import { useQuery } from 'react-query';
import { Shield, FileText, AlertTriangle, TrendingUp } from 'lucide-react';

const Dashboard: React.FC = () => {
  // Mock data for now - will be replaced with actual API calls
  const { data: stats, isLoading } = useQuery('dashboard-stats', async () => {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    return {
      totalDocuments: 1247,
      fraudDetected: 23,
      highRiskDocuments: 8,
      processingTime: 87
    };
  });

  const { data: recentDocuments } = useQuery('recent-documents', async () => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return [
      {
        id: '1',
        filename: 'invoice_001.pdf',
        fraudScore: 0.15,
        riskLevel: 'low',
        uploadedAt: '2024-01-15T10:30:00Z'
      },
      {
        id: '2',
        filename: 'loan_application_002.pdf',
        fraudScore: 0.85,
        riskLevel: 'high',
        uploadedAt: '2024-01-15T09:15:00Z'
      },
      {
        id: '3',
        filename: 'bank_statement_003.pdf',
        fraudScore: 0.45,
        riskLevel: 'medium',
        uploadedAt: '2024-01-15T08:45:00Z'
      }
    ];
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

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
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Monitor document fraud detection in real-time</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="document-card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <FileText className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Documents</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.totalDocuments}</p>
            </div>
          </div>
        </div>

        <div className="document-card">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <Shield className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Fraud Detected</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.fraudDetected}</p>
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
              <p className="text-2xl font-bold text-gray-900">{stats?.highRiskDocuments}</p>
            </div>
          </div>
        </div>

        <div className="document-card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg. Processing</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.processingTime}ms</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Documents */}
      <div className="document-card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Documents</h2>
        <div className="space-y-3">
          {recentDocuments?.map((doc) => (
            <div key={doc.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-4">
                <FileText className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="font-medium text-gray-900">{doc.filename}</p>
                  <p className="text-sm text-gray-500">
                    Uploaded {new Date(doc.uploadedAt).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelColor(doc.riskLevel)}`}>
                  {doc.riskLevel.toUpperCase()}
                </span>
                <span className="text-sm font-medium text-gray-900">
                  {(doc.fraudScore * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
