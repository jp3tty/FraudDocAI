package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"frauddocai-backend/services"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

// Global service instances
var minioService *services.MinIOService
var dbService *services.DatabaseService

func main() {
	// Initialize MinIO service
	var err error
	minioService, err = services.NewMinIOService()
	if err != nil {
		log.Fatalf("Failed to initialize MinIO service: %v", err)
	}
	log.Println("MinIO service initialized successfully")

	// Initialize Database service
	dbService, err = services.NewDatabaseService()
	if err != nil {
		log.Fatalf("Failed to initialize database service: %v", err)
	}
	log.Println("Database service initialized successfully")

	// Initialize Gin router
	r := gin.Default()

	// CORS middleware
	config := cors.DefaultConfig()
	config.AllowOrigins = []string{"http://localhost:3000", "http://localhost:8080"}
	config.AllowMethods = []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"}
	config.AllowHeaders = []string{"Origin", "Content-Type", "Accept", "Authorization"}
	r.Use(cors.New(config))

	// Routes
	setupRoutes(r)

	// Get port from environment or use default
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Starting FraudDocAI Backend on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}

func setupRoutes(r *gin.Engine) {
	// Health check
	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"service": "FraudDocAI Backend",
			"status":  "running",
			"version": "1.0.0",
		})
	})

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":    "healthy",
			"timestamp": "2024-01-01T00:00:00Z",
		})
	})

	// API v1 routes
	v1 := r.Group("/api/v1")
	{
		// Document routes
		documents := v1.Group("/documents")
		{
			documents.POST("/upload", uploadDocument)
			documents.GET("/", getDocuments)
			documents.GET("/:id", getDocument)
			documents.DELETE("/:id", deleteDocument)
		}

		// Fraud detection routes
		fraud := v1.Group("/fraud")
		{
			fraud.POST("/analyze", analyzeDocument)
			fraud.GET("/patterns", getFraudPatterns)
			fraud.GET("/reports", getFraudReports)
		}

		// User routes
		users := v1.Group("/users")
		{
			users.POST("/register", registerUser)
			users.POST("/login", loginUser)
			users.GET("/profile", getUserProfile)
		}
	}
}

// Document handlers
func uploadDocument(c *gin.Context) {
	// Get the file from the form
	file, header, err := c.Request.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":  "No file uploaded",
			"status": "error",
		})
		return
	}
	defer file.Close()

	// Generate unique filename
	objectName := fmt.Sprintf("%d_%s", time.Now().Unix(), header.Filename)

	// Upload to MinIO
	ctx := context.Background()
	err = minioService.UploadFile(ctx, objectName, file, header.Size, header.Header.Get("Content-Type"))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":  "Failed to upload file",
			"status": "error",
		})
		return
	}

	// Save document metadata to database
	document := &services.Document{
		Filename:         objectName,
		OriginalFilename: header.Filename,
		FilePath:         objectName,
		FileSize:         header.Size,
		MimeType:         header.Header.Get("Content-Type"),
		Status:           "uploaded",
		FraudRiskLevel:   "low",
	}

	err = dbService.CreateDocument(document)
	if err != nil {
		log.Printf("Failed to save document to database: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":  fmt.Sprintf("Failed to save document to database: %v", err),
			"status": "error",
		})
		return
	}
	log.Printf("Document saved to database with ID: %s", document.ID)

	// Extract text from document for analysis
	extractedText, err := extractTextFromFile(file, header.Header.Get("Content-Type"))
	if err != nil {
		log.Printf("Failed to extract text from document: %v", err)
		extractedText = "Text extraction failed"
	}

	// Trigger fraud analysis in background
	go func() {
		err := analyzeDocumentForFraud(document.ID, extractedText)
		if err != nil {
			log.Printf("Fraud analysis failed for document %s: %v", document.ID, err)
		}
	}()

	c.JSON(http.StatusOK, gin.H{
		"message":   "File uploaded successfully",
		"file_id":   document.ID,
		"file_name": header.Filename,
		"file_size": header.Size,
		"file_url":  minioService.GetFileURL(objectName),
		"status":    "success",
	})
}

func getDocuments(c *gin.Context) {
	// Get pagination parameters
	limitStr := c.DefaultQuery("limit", "10")
	offsetStr := c.DefaultQuery("offset", "0")

	limit, err := strconv.Atoi(limitStr)
	if err != nil {
		limit = 10
	}

	offset, err := strconv.Atoi(offsetStr)
	if err != nil {
		offset = 0
	}

	// Get documents from database
	documents, err := dbService.GetDocuments(limit, offset)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":  "Failed to retrieve documents",
			"status": "error",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"documents": documents,
		"total":     len(documents),
		"status":    "success",
	})
}

func getDocument(c *gin.Context) {
	documentID := c.Param("id")

	document, err := dbService.GetDocument(documentID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error":  "Document not found",
			"status": "error",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"document": document,
		"status":   "success",
	})
}

func deleteDocument(c *gin.Context) {
	// TODO: Implement delete document
	documentID := c.Param("id")
	c.JSON(http.StatusOK, gin.H{
		"message":     "Document deleted",
		"document_id": documentID,
		"status":      "success",
	})
}

// Fraud detection handlers
func analyzeDocument(c *gin.Context) {
	// TODO: Implement fraud analysis
	c.JSON(http.StatusOK, gin.H{
		"message": "Fraud analysis endpoint - TODO: implement",
		"status":  "success",
	})
}

func getFraudPatterns(c *gin.Context) {
	// TODO: Implement get fraud patterns
	patterns := []gin.H{
		{
			"id":          "signature_forgery",
			"name":        "Signature Forgery",
			"description": "Detects potentially forged signatures",
			"severity":    "high",
		},
		{
			"id":          "amount_tampering",
			"name":        "Amount Tampering",
			"description": "Detects altered monetary amounts",
			"severity":    "critical",
		},
	}

	c.JSON(http.StatusOK, gin.H{
		"patterns": patterns,
		"total":    len(patterns),
		"status":   "success",
	})
}

func getFraudReports(c *gin.Context) {
	// TODO: Implement get fraud reports
	c.JSON(http.StatusOK, gin.H{
		"reports": []gin.H{},
		"total":   0,
		"status":  "success",
	})
}

// User handlers
func registerUser(c *gin.Context) {
	// TODO: Implement user registration
	c.JSON(http.StatusOK, gin.H{
		"message": "User registration endpoint - TODO: implement",
		"status":  "success",
	})
}

func loginUser(c *gin.Context) {
	// TODO: Implement user login
	c.JSON(http.StatusOK, gin.H{
		"message": "User login endpoint - TODO: implement",
		"status":  "success",
	})
}

func getUserProfile(c *gin.Context) {
	// TODO: Implement get user profile
	c.JSON(http.StatusOK, gin.H{
		"message": "User profile endpoint - TODO: implement",
		"status":  "success",
	})
}

// Helper function to extract text from uploaded file
func extractTextFromFile(file io.Reader, contentType string) (string, error) {
	// For now, handle text files only
	if contentType == "text/plain" {
		var buf bytes.Buffer
		_, err := buf.ReadFrom(file)
		if err != nil {
			return "", err
		}
		return buf.String(), nil
	}

	// For other file types, return placeholder text
	return "Document content extraction not implemented for " + contentType, nil
}

// Fraud analysis function that calls AI service
func analyzeDocumentForFraud(documentID, text string) error {
	// Prepare request to AI service
	requestBody := map[string]string{
		"text": text,
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		return fmt.Errorf("failed to marshal request: %v", err)
	}

	// Call AI service
	resp, err := http.Post("http://localhost:8001/analyze-text", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("failed to call AI service: %v", err)
	}
	defer resp.Body.Close()

	// Read response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read AI service response: %v", err)
	}

	// Parse response
	var analysisResult map[string]interface{}
	if err := json.Unmarshal(body, &analysisResult); err != nil {
		return fmt.Errorf("failed to parse AI service response: %v", err)
	}

	// Extract fraud score and risk level
	fraudScore, ok := analysisResult["fraud_score"].(float64)
	if !ok {
		fraudScore = 0.0
	}

	riskLevel, ok := analysisResult["fraud_risk_level"].(string)
	if !ok {
		riskLevel = "unknown"
	}

	// Update document in database with fraud analysis results
	err = dbService.UpdateDocumentFraudAnalysis(documentID, fraudScore, riskLevel, text)
	if err != nil {
		return fmt.Errorf("failed to update document with fraud analysis: %v", err)
	}

	log.Printf("Fraud analysis completed for document %s: score=%.3f, risk=%s", documentID, fraudScore, riskLevel)
	return nil
}
