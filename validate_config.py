#!/usr/bin/env python3
"""
Configuration validation script
Checks if all required environment variables are properly set
"""

import os
import sys
from pathlib import Path

def validate_config():
    """Validate configuration and print status"""
    print("🔍 Validating MLOps Pipeline Configuration")
    print("=" * 50)
    
    # Check if config file exists
    config_file = Path("config.env")
    if config_file.exists():
        print("✅ Configuration file found: config.env")
    else:
        print("ℹ️  No config.env found, using defaults")
        print("   To customize: cp config.env.example config.env")
    
    # Import and test config
    try:
        from config import get_config
        config = get_config()
        print("✅ Configuration module loaded successfully")
        
        # Test key configurations
        print(f"📊 MLflow Tracking URI: {config.mlflow_tracking_uri}")
        print(f"🌐 Airflow UI: {config.airflow_ui_url}")
        print(f"📈 Streamlit Dashboard: {config.streamlit_ui_url}")
        print(f"☕ Java Home: {config.java_home}")
        print(f"🗄️  Airflow Home: {config.airflow_home}")
        
        # Check if paths exist
        paths_to_check = [
            ("Data Raw Path", config.data_raw_path),
            ("Delta Bronze", config.data_delta_bronze),
            ("Delta Silver", config.data_delta_silver),
            ("Delta Gold", config.data_delta_gold),
            ("Output Predictions", config.output_predictions_path)
        ]
        
        print("\n📁 Path Validation:")
        for name, path in paths_to_check:
            if Path(path).exists():
                print(f"✅ {name}: {path}")
            else:
                print(f"⚠️  {name}: {path} (will be created)")
        
        print("\n🎯 Configuration Summary:")
        print(f"   • MLflow: {config.mlflow_tracking_uri}")
        print(f"   • Airflow: {config.airflow_ui_url}")
        print(f"   • Dashboard: {config.streamlit_ui_url}")
        print(f"   • Model: {config.model_name} ({config.model_stage})")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

if __name__ == "__main__":
    success = validate_config()
    sys.exit(0 if success else 1)
