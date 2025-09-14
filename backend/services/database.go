package services

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/lib/pq"
)

type DatabaseService struct {
	db *sql.DB
}

type Document struct {
	ID               string    `json:"id"`
	UserID           *string   `json:"user_id"`
	Filename         string    `json:"filename"`
	OriginalFilename string    `json:"original_filename"`
	FilePath         string    `json:"file_path"`
	FileSize         int64     `json:"file_size"`
	MimeType         string    `json:"mime_type"`
	DocumentType     *string   `json:"document_type"`
	Status           string    `json:"status"`
	FraudScore       *float64  `json:"fraud_score"`
	FraudRiskLevel   string    `json:"fraud_risk_level"`
	ExtractedText    *string   `json:"extracted_text"`
	EmotionAnalysis  *string   `json:"emotion_analysis"`
	PatternAnalysis  *string   `json:"pattern_analysis"`
	Metadata         *string   `json:"metadata"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type FraudDetection struct {
	ID               string     `json:"id"`
	DocumentID       string     `json:"document_id"`
	FraudPatternID   *string    `json:"fraud_pattern_id"`
	ConfidenceScore  float64    `json:"confidence_score"`
	DetectionDetails *string    `json:"detection_details"`
	IsFalsePositive  bool       `json:"is_false_positive"`
	ReviewedBy       *string    `json:"reviewed_by"`
	ReviewedAt       *time.Time `json:"reviewed_at"`
	CreatedAt        time.Time  `json:"created_at"`
}

func NewDatabaseService() (*DatabaseService, error) {
	// Database connection string
	connStr := "host=localhost port=5432 user=frauddocai password=frauddocai123 dbname=frauddocai sslmode=disable"

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %v", err)
	}

	// Test the connection
	if err := db.Ping(); err != nil {
		return nil, fmt.Errorf("failed to ping database: %v", err)
	}

	// Set connection pool settings
	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(25)
	db.SetConnMaxLifetime(5 * time.Minute)

	log.Println("Database connection established successfully")

	return &DatabaseService{db: db}, nil
}

func (d *DatabaseService) Close() error {
	return d.db.Close()
}

// Document operations
func (d *DatabaseService) CreateDocument(doc *Document) error {
	query := `
		INSERT INTO documents (
			user_id, filename, original_filename, file_path, file_size,
			mime_type, document_type, status, fraud_score, fraud_risk_level,
			extracted_text, emotion_analysis, pattern_analysis, metadata
		) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
		RETURNING id, created_at, updated_at`

	err := d.db.QueryRow(
		query,
		doc.UserID, doc.Filename, doc.OriginalFilename, doc.FilePath,
		doc.FileSize, doc.MimeType, doc.DocumentType, doc.Status,
		doc.FraudScore, doc.FraudRiskLevel, doc.ExtractedText, doc.EmotionAnalysis, doc.PatternAnalysis, doc.Metadata,
	).Scan(&doc.ID, &doc.CreatedAt, &doc.UpdatedAt)

	return err
}

func (d *DatabaseService) GetDocument(id string) (*Document, error) {
	query := `
		SELECT id, user_id, filename, original_filename, file_path, file_size,
		       mime_type, document_type, status, fraud_score, fraud_risk_level,
		       extracted_text, emotion_analysis, pattern_analysis, metadata, created_at, updated_at
		FROM documents WHERE id = $1`

	doc := &Document{}
	err := d.db.QueryRow(query, id).Scan(
		&doc.ID, &doc.UserID, &doc.Filename, &doc.OriginalFilename,
		&doc.FilePath, &doc.FileSize, &doc.MimeType, &doc.DocumentType,
		&doc.Status, &doc.FraudScore, &doc.FraudRiskLevel,
		&doc.ExtractedText, &doc.EmotionAnalysis, &doc.PatternAnalysis, &doc.Metadata, &doc.CreatedAt, &doc.UpdatedAt,
	)

	if err != nil {
		return nil, err
	}

	return doc, nil
}

func (d *DatabaseService) UpdateDocumentFraudAnalysis(id string, fraudScore float64, riskLevel string, extractedText string, emotionAnalysis, patternAnalysis string) error {
	query := `
		UPDATE documents 
		SET fraud_score = $2, fraud_risk_level = $3, extracted_text = $4, 
		    emotion_analysis = $5, pattern_analysis = $6, status = 'processed', updated_at = CURRENT_TIMESTAMP
		WHERE id = $1`

	_, err := d.db.Exec(query, id, fraudScore, riskLevel, extractedText, emotionAnalysis, patternAnalysis)
	return err
}

func (d *DatabaseService) CreateFraudDetection(detection *FraudDetection) error {
	query := `
		INSERT INTO document_fraud_detections (
			document_id, fraud_pattern_id, confidence_score, 
			detection_details, is_false_positive, reviewed_by, reviewed_at
		) VALUES ($1, $2, $3, $4, $5, $6, $7)
		RETURNING id, created_at`

	err := d.db.QueryRow(
		query,
		detection.DocumentID, detection.FraudPatternID, detection.ConfidenceScore,
		detection.DetectionDetails, detection.IsFalsePositive,
		detection.ReviewedBy, detection.ReviewedAt,
	).Scan(&detection.ID, &detection.CreatedAt)

	return err
}

func (d *DatabaseService) GetDocuments(limit, offset int) ([]*Document, error) {
	query := `
		SELECT id, user_id, filename, original_filename, file_path, file_size,
		       mime_type, document_type, status, fraud_score, fraud_risk_level,
		       extracted_text, emotion_analysis, pattern_analysis, metadata, created_at, updated_at
		FROM documents 
		ORDER BY created_at DESC 
		LIMIT $1 OFFSET $2`

	rows, err := d.db.Query(query, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var documents []*Document
	for rows.Next() {
		doc := &Document{}
		err := rows.Scan(
			&doc.ID, &doc.UserID, &doc.Filename, &doc.OriginalFilename,
			&doc.FilePath, &doc.FileSize, &doc.MimeType, &doc.DocumentType,
			&doc.Status, &doc.FraudScore, &doc.FraudRiskLevel,
			&doc.ExtractedText, &doc.EmotionAnalysis, &doc.PatternAnalysis, &doc.Metadata, &doc.CreatedAt, &doc.UpdatedAt,
		)
		if err != nil {
			return nil, err
		}
		documents = append(documents, doc)
	}

	return documents, nil
}
