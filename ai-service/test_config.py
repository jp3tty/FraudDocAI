#!/usr/bin/env python3
"""
Test script to demonstrate FraudDocAI AI Service configuration
"""

import os
import sys
from config import config

def test_default_config():
    """Test default configuration"""
    print("🔧 Testing Default Configuration")
    print("=" * 50)
    
    server_config = config.get_server_config()
    cors_config = config.get_cors_config()
    ai_config = config.get_ai_config()
    
    print(f"Server Host: {server_config['host']}")
    print(f"Server Port: {server_config['port']}")
    print(f"Auto Reload: {server_config['reload']}")
    print(f"Log Level: {server_config['log_level']}")
    print(f"CORS Origins: {cors_config['allow_origins']}")
    print(f"Emotion Model: {ai_config['emotion_model']}")
    print(f"QA Model: {ai_config['qa_model']}")
    print(f"Embedding Model: {ai_config['embedding_model']}")
    
    # Test dynamic URL building
    print(f"Base URL: {config.get_base_url()}")
    print(f"Health URL: {config.get_health_url()}")
    print()

def test_environment_override():
    """Test environment variable override"""
    print("🌍 Testing Environment Variable Override")
    print("=" * 50)
    
    # Set environment variables
    os.environ['FRAUDDOCAI_PORT'] = '9001'
    os.environ['FRAUDDOCAI_HOST'] = '127.0.0.1'
    os.environ['FRAUDDOCAI_LOG_LEVEL'] = 'debug'
    
    # Reload config to pick up environment variables
    from importlib import reload
    import config
    reload(config)
    config = config.config
    
    server_config = config.get_server_config()
    
    print(f"Server Host: {server_config['host']} (should be 127.0.0.1)")
    print(f"Server Port: {server_config['port']} (should be 9001)")
    print(f"Log Level: {server_config['log_level']} (should be debug)")
    print()

def test_config_file():
    """Test configuration file loading"""
    print("📁 Testing Configuration File Loading")
    print("=" * 50)
    
    # Check if config.ini exists
    if os.path.exists('config.ini'):
        print("✅ config.ini found")
        with open('config.ini', 'r') as f:
            print("Configuration file contents:")
            print(f.read())
    else:
        print("❌ config.ini not found")
        print("Run: cp config.example.ini config.ini")
    print()

def test_health_endpoint():
    """Test health endpoint configuration display"""
    print("🏥 Testing Health Endpoint Configuration")
    print("=" * 50)
    
    try:
        import requests
        # Get dynamic health URL from configuration
        health_url = config.get_health_url()
        print(f"Testing health endpoint: {health_url}")
        
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ AI Service is running")
            print(f"Status: {data['status']}")
            if 'configuration' in data:
                print("Configuration from API:")
                print(f"  Host: {data['configuration']['server']['host']}")
                print(f"  Port: {data['configuration']['server']['port']}")
                print(f"  Log Level: {data['configuration']['server']['log_level']}")
        else:
            print(f"❌ AI Service returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ AI Service is not running")
        print("Start it with: python app.py")
    except ImportError:
        print("❌ requests library not installed")
        print("Install with: pip install requests")
    print()

def main():
    """Run all configuration tests"""
    print("🚀 FraudDocAI AI Service Configuration Test")
    print("=" * 60)
    print()
    
    test_default_config()
    test_environment_override()
    test_config_file()
    test_health_endpoint()
    
    print("✅ Configuration testing complete!")
    print()
    print("📚 For more configuration options, see CONFIGURATION.md")

if __name__ == "__main__":
    main()
