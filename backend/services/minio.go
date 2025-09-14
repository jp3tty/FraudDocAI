package services

import (
    "context"
    "fmt"
    "io"
    "log"

    "frauddocai-backend/config"
    "github.com/minio/minio-go/v7"
    "github.com/minio/minio-go/v7/pkg/credentials"
)

type MinIOService struct {
    client *minio.Client
    bucket string
}

func NewMinIOService() (*MinIOService, error) {
    cfg := config.GetMinIOConfig()
    
    client, err := minio.New(cfg.Endpoint, &minio.Options{
        Creds:  credentials.NewStaticV4(cfg.AccessKeyID, cfg.SecretAccessKey, ""),
        Secure: cfg.UseSSL,
    })
    if err != nil {
        return nil, err
    }

    service := &MinIOService{
        client: client,
        bucket: cfg.BucketName,
    }

    // Create bucket if it doesn't exist
    ctx := context.Background()
    exists, err := client.BucketExists(ctx, cfg.BucketName)
    if err != nil {
        return nil, err
    }
    
    if !exists {
        err = client.MakeBucket(ctx, cfg.BucketName, minio.MakeBucketOptions{})
        if err != nil {
            return nil, err
        }
        log.Printf("Created bucket: %s", cfg.BucketName)
    }

    return service, nil
}

func (m *MinIOService) UploadFile(ctx context.Context, objectName string, reader io.Reader, size int64, contentType string) error {
    _, err := m.client.PutObject(ctx, m.bucket, objectName, reader, size, minio.PutObjectOptions{
        ContentType: contentType,
    })
    return err
}

func (m *MinIOService) GetFile(ctx context.Context, objectName string) (*minio.Object, error) {
    return m.client.GetObject(ctx, m.bucket, objectName, minio.GetObjectOptions{})
}

func (m *MinIOService) DeleteFile(ctx context.Context, objectName string) error {
    return m.client.RemoveObject(ctx, m.bucket, objectName, minio.RemoveObjectOptions{})
}

func (m *MinIOService) GetFileURL(objectName string) string {
    return fmt.Sprintf("http://localhost:9000/%s/%s", m.bucket, objectName)
}