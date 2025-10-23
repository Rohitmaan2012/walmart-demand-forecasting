#!/usr/bin/env python3
"""
Configuration management for Walmart MLOps pipeline
Handles environment variables and configuration with proper defaults
"""

import os
from pathlib import Path
from typing import Optional

class Config:
    """Centralized configuration management"""
    
    def __init__(self):
        self._load_env_file()
    
    def _load_env_file(self):
        """Load environment variables from config.env if it exists"""
        env_file = Path("config.env")
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    # MLflow Configuration
    @property
    def mlflow_tracking_uri(self) -> str:
        return os.getenv("MLFLOW_TRACKING_URI", "file://./mlruns")
    
    @property
    def mlflow_backend_store_uri(self) -> str:
        return os.getenv("MLFLOW_BACKEND_STORE_URI", "file://./mlruns")
    
    @property
    def mlflow_artifact_root(self) -> str:
        return os.getenv("MLFLOW_ARTIFACT_ROOT", "./artifacts")
    
    # Airflow Configuration
    @property
    def airflow_home(self) -> str:
        return os.getenv("AIRFLOW_HOME", "./.airflow")
    
    @property
    def airflow_webserver_port(self) -> int:
        return int(os.getenv("AIRFLOW_WEBSERVER_PORT", "8080"))
    
    @property
    def airflow_webserver_host(self) -> str:
        return os.getenv("AIRFLOW_WEBSERVER_HOST", "127.0.0.1")
    
    @property
    def airflow_admin_username(self) -> str:
        return os.getenv("AIRFLOW_ADMIN_USERNAME", "admin")
    
    @property
    def airflow_admin_password(self) -> str:
        return os.getenv("AIRFLOW_ADMIN_PASSWORD", "admin")
    
    @property
    def airflow_admin_email(self) -> str:
        return os.getenv("AIRFLOW_ADMIN_EMAIL", "admin@example.com")
    
    @property
    def airflow_admin_firstname(self) -> str:
        return os.getenv("AIRFLOW_ADMIN_FIRSTNAME", "Admin")
    
    @property
    def airflow_admin_lastname(self) -> str:
        return os.getenv("AIRFLOW_ADMIN_LASTNAME", "User")
    
    # Streamlit Configuration
    @property
    def streamlit_port(self) -> int:
        return int(os.getenv("STREAMLIT_PORT", "8501"))
    
    @property
    def streamlit_host(self) -> str:
        return os.getenv("STREAMLIT_HOST", "127.0.0.1")
    
    # Java Configuration
    @property
    def java_home(self) -> str:
        return os.getenv("JAVA_HOME", "/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home")
    
    # Spark Configuration
    @property
    def spark_master(self) -> str:
        return os.getenv("SPARK_MASTER", "local[*]")
    
    @property
    def spark_app_name(self) -> str:
        return os.getenv("SPARK_APP_NAME", "walmart-mlops")
    
    # Model Configuration
    @property
    def model_name(self) -> str:
        return os.getenv("MODEL_NAME", "demand_gbt")
    
    @property
    def model_stage(self) -> str:
        return os.getenv("MODEL_STAGE", "Production")
    
    @property
    def prediction_horizon_days(self) -> int:
        return int(os.getenv("PREDICTION_HORIZON_DAYS", "7"))
    
    # Data Paths
    @property
    def data_raw_path(self) -> str:
        return os.getenv("DATA_RAW_PATH", "./data/raw")
    
    @property
    def data_delta_bronze(self) -> str:
        return os.getenv("DATA_DELTA_BRONZE", "./data/delta/bronze")
    
    @property
    def data_delta_silver(self) -> str:
        return os.getenv("DATA_DELTA_SILVER", "./data/delta/silver")
    
    @property
    def data_delta_gold(self) -> str:
        return os.getenv("DATA_DELTA_GOLD", "./data/delta/gold")
    
    @property
    def output_predictions_path(self) -> str:
        return os.getenv("OUTPUT_PREDICTIONS_PATH", "./outputs/predictions")
    
    # Computed Properties
    @property
    def airflow_ui_url(self) -> str:
        return f"http://{self.airflow_webserver_host}:{self.airflow_webserver_port}"
    
    @property
    def streamlit_ui_url(self) -> str:
        return f"http://{self.streamlit_host}:{self.streamlit_port}"
    
    @property
    def mlflow_ui_url(self) -> str:
        return f"http://{self.streamlit_host}:5001"  # MLflow typically uses 5001
    
    def get_airflow_webserver_command(self) -> str:
        """Get the airflow webserver command with configured parameters"""
        return f"airflow webserver -p {self.airflow_webserver_port} -H {self.airflow_webserver_host}"
    
    def get_streamlit_command(self) -> str:
        """Get the streamlit command with configured parameters"""
        return f"streamlit run dashboard.py --server.port {self.streamlit_port} --server.address {self.streamlit_host}"
    
    def get_mlflow_ui_command(self) -> str:
        """Get the MLflow UI command with configured parameters"""
        return f"mlflow ui --backend-store-uri {self.mlflow_backend_store_uri} --host {self.streamlit_host} --port 5001"

# Global config instance
config = Config()

def get_config() -> Config:
    """Get the global configuration instance"""
    return config
