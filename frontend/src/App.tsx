import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import './App.css';

// Components
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import DocumentUpload from './pages/DocumentUpload';
import FraudAnalysis from './pages/FraudAnalysis';
import DocumentQA from './pages/DocumentQA';
import Reports from './pages/Reports';

// Create a client
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/upload" element={<DocumentUpload />} />
              <Route path="/analysis" element={<FraudAnalysis />} />
              <Route path="/qa" element={<DocumentQA />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </main>
          <Toaster position="top-right" />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
