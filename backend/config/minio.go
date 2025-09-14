package config

import (
    "os"
)

type MinIOConfig struct {
    Endpoint        string
    AccessKeyID     string
    SecretAccessKey string
    UseSSL          bool
    BucketName      string
}

func GetMinIOConfig() MinIOConfig {
    return MinIOConfig{
        Endpoint:        getEnv("MINIO_ENDPOINT", "localhost:9000"),
        AccessKeyID:     getEnv("MINIO_ACCESS_KEY", "frauddocai"),
        SecretAccessKey: getEnv("MINIO_SECRET_KEY", "frauddocai123"),
        UseSSL:          false,
        BucketName:      getEnv("MINIO_BUCKET", "documents"),
    }
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}