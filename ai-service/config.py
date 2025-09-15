"""
FraudDocAI - AI Service Configuration
Configuration management with environment variable support
"""

import os
from configparser import ConfigParser
from typing import Dict, Any, List

class Config:
    """Configuration management with environment variable support"""
    
    def __init__(self):
        self.config = ConfigParser()
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file and environment variables"""
        # Default configuration
        self.config['server'] = {
            'host': '0.0.0.0',
            'port': '8001',
            'reload': 'true',
            'log_level': 'info'
        }
        
        self.config['cors'] = {
            'allowed_origins': 'http://localhost:3000,http://localhost:8080',
            'allow_credentials': 'true'
        }
        
        self.config['ai'] = {
            'emotion_model': 'cardiffnlp/twitter-roberta-base-emotion',
            'qa_model': 'distilbert-base-uncased-distilled-squad',
            'embedding_model': 'all-MiniLM-L6-v2'
        }
        
        # Try to load from config file
        config_file = os.getenv('FRAUDDOCAI_CONFIG', 'config.ini')
        if os.path.exists(config_file):
            self.config.read(config_file)
        
        # Override with environment variables
        self._apply_env_overrides()
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides"""
        # Server configuration
        if os.getenv('FRAUDDOCAI_HOST'):
            self.config['server']['host'] = os.getenv('FRAUDDOCAI_HOST')
        if os.getenv('FRAUDDOCAI_PORT'):
            self.config['server']['port'] = os.getenv('FRAUDDOCAI_PORT')
        if os.getenv('FRAUDDOCAI_RELOAD'):
            self.config['server']['reload'] = os.getenv('FRAUDDOCAI_RELOAD')
        if os.getenv('FRAUDDOCAI_LOG_LEVEL'):
            self.config['server']['log_level'] = os.getenv('FRAUDDOCAI_LOG_LEVEL')
        
        # CORS configuration
        if os.getenv('FRAUDDOCAI_CORS_ORIGINS'):
            self.config['cors']['allowed_origins'] = os.getenv('FRAUDDOCAI_CORS_ORIGINS')
        if os.getenv('FRAUDDOCAI_CORS_CREDENTIALS'):
            self.config['cors']['allow_credentials'] = os.getenv('FRAUDDOCAI_CORS_CREDENTIALS')
        
        # AI model configuration
        if os.getenv('FRAUDDOCAI_EMOTION_MODEL'):
            self.config['ai']['emotion_model'] = os.getenv('FRAUDDOCAI_EMOTION_MODEL')
        if os.getenv('FRAUDDOCAI_QA_MODEL'):
            self.config['ai']['qa_model'] = os.getenv('FRAUDDOCAI_QA_MODEL')
        if os.getenv('FRAUDDOCAI_EMBEDDING_MODEL'):
            self.config['ai']['embedding_model'] = os.getenv('FRAUDDOCAI_EMBEDDING_MODEL')
    
    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration"""
        return {
            'host': self.config['server']['host'],
            'port': int(self.config['server']['port']),
            'reload': self.config['server']['reload'].lower() == 'true',
            'log_level': self.config['server']['log_level']
        }
    
    def get_cors_config(self) -> Dict[str, Any]:
        """Get CORS configuration"""
        origins = [origin.strip() for origin in self.config['cors']['allowed_origins'].split(',')]
        return {
            'allow_origins': origins,
            'allow_credentials': self.config['cors']['allow_credentials'].lower() == 'true',
            'allow_methods': ["*"],
            'allow_headers': ["*"]
        }
    
    def get_ai_config(self) -> Dict[str, str]:
        """Get AI model configuration"""
        return {
            'emotion_model': self.config['ai']['emotion_model'],
            'qa_model': self.config['ai']['qa_model'],
            'embedding_model': self.config['ai']['embedding_model']
        }
    
    def save_config(self, filename: str = 'config.ini'):
        """Save current configuration to file"""
        with open(filename, 'w') as f:
            self.config.write(f)
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            'server': self.get_server_config(),
            'cors': self.get_cors_config(),
            'ai': self.get_ai_config()
        }
    
    def get_base_url(self, protocol: str = "http") -> str:
        """Get base URL for the service"""
        server_config = self.get_server_config()
        return f"{protocol}://{server_config['host']}:{server_config['port']}"
    
    def get_health_url(self, protocol: str = "http") -> str:
        """Get health check URL for the service"""
        return f"{self.get_base_url(protocol)}/health"

# Global config instance
config = Config()
