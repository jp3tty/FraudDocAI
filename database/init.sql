-- FraudDocAI Database Schema
-- Initialize the database with required tables

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    document_type VARCHAR(50), -- invoice, receipt, bank_statement, loan_application
    status VARCHAR(50) DEFAULT 'uploaded', -- uploaded, processing, processed, failed
    fraud_score DECIMAL(5,2) DEFAULT 0.00,
    fraud_risk_level VARCHAR(20) DEFAULT 'low', -- low, medium, high, critical
    extracted_text TEXT,
    emotion_analysis JSONB, -- Store emotion analysis results
    pattern_analysis JSONB, -- Store pattern analysis results
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document embeddings for semantic search (using JSONB for now)
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    embedding_data JSONB, -- Store embeddings as JSON for now
    embedding_type VARCHAR(50) NOT NULL, -- text, metadata, fraud_pattern
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fraud patterns table
CREATE TABLE fraud_patterns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pattern_name VARCHAR(255) NOT NULL,
    pattern_type VARCHAR(100) NOT NULL, -- signature_forgery, amount_tampering, duplicate_invoice
    description TEXT,
    detection_rules JSONB,
    severity VARCHAR(20) DEFAULT 'medium',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document fraud detections
CREATE TABLE document_fraud_detections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    fraud_pattern_id UUID REFERENCES fraud_patterns(id),
    confidence_score DECIMAL(5,2) NOT NULL,
    detection_details JSONB,
    is_false_positive BOOLEAN DEFAULT false,
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions for behavioral analysis
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    actions JSONB, -- Track user interactions
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Audit log for compliance
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    details JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_fraud_score ON documents(fraud_score);
CREATE INDEX idx_documents_created_at ON documents(created_at);
CREATE INDEX idx_document_embeddings_document_id ON document_embeddings(document_id);
CREATE INDEX idx_document_fraud_detections_document_id ON document_fraud_detections(document_id);
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- JSONB index for embedding search
CREATE INDEX idx_document_embeddings_data ON document_embeddings USING gin (embedding_data);

-- Insert default fraud patterns
INSERT INTO fraud_patterns (pattern_name, pattern_type, description, detection_rules, severity) VALUES
('Signature Forgery', 'signature_forgery', 'Detects potentially forged signatures on documents', '{"ml_model": "signature_verification", "threshold": 0.8}', 'high'),
('Amount Tampering', 'amount_tampering', 'Detects altered monetary amounts in documents', '{"pattern_matching": true, "ocr_confidence_threshold": 0.9}', 'critical'),
('Duplicate Invoice', 'duplicate_invoice', 'Identifies duplicate or near-duplicate invoices', '{"similarity_threshold": 0.95, "check_fields": ["vendor", "amount", "date"]}', 'medium'),
('Fake Vendor', 'fake_vendor', 'Detects potentially fake vendor information', '{"vendor_verification": true, "domain_check": true}', 'high'),
('Inconsistent Data', 'inconsistent_data', 'Flags documents with inconsistent information', '{"cross_field_validation": true, "date_consistency": true}', 'medium');

-- Create a default admin user (password: admin123)
INSERT INTO users (email, password_hash, first_name, last_name, role) VALUES
('admin@frauddocai.com', crypt('admin123', gen_salt('bf')), 'Admin', 'User', 'admin');

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_fraud_patterns_updated_at BEFORE UPDATE ON fraud_patterns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
