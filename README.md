# 🎯 Walmart Demand Forecasting (MLflow + Airflow + Delta Lake)

**Production-ready MLOps pipeline for retail sales forecasting using real Kaggle Walmart data.**

## 🚀 Quickstart

### 1. Setup Environment
```bash
make venv
```

### 2. Run the Complete Pipeline
```bash
# Process Walmart data and train model
make etl
make train
make infer
```

### 3. View Results
- **Streamlit Dashboard**: `./start_dashboard.sh` then open the displayed URL
- **Airflow UI**: `./start_airflow.sh` then open the displayed URL (admin/admin)
- **MLflow UI**: `make mlflow` for the command, or use the Streamlit dashboard

### 4. Configuration (Optional)
- **Customize settings**: Copy `config.env.example` to `config.env` and modify
- **Environment variables**: All URLs, ports, and paths are configurable
- **Default values**: Works out-of-the-box with sensible defaults

## 📊 Dataset & Features

**Data Source**: Kaggle Walmart Store Sales Forecasting (6,436 rows, 2010-2012)
- **Stores**: Multiple Walmart locations
- **Granularity**: Weekly sales data
- **Target**: Weekly sales dollars
- **Features**: Holiday flags, temperature, fuel price, CPI, unemployment

## 🏗️ Architecture

### Data Pipeline
```
Walmart.csv → PySpark ETL → Delta Lake → GBT Model → MLflow → Airflow → Predictions
     ↓              ↓           ↓           ↓         ↓        ↓         ↓
  Raw Data    Feature Eng.  Gold Layer  Training  Tracking  Orchestr.  Output
```

### Lakehouse Layers
- **Bronze**: Raw Walmart CSV ingestion
- **Silver**: Data cleaning, schema mapping, date parsing
- **Gold**: Feature engineering with weekly lags and economic indicators

## 📈 Model Performance

- **Algorithm**: Spark GBTRegressor
- **Features**: Weekly lags (1w, 4w, 8w), moving averages, economic indicators
- **Performance**: RMSE=118,622, MAE=65,165
- **Target**: Weekly sales forecasting

## 📁 Outputs

- **Delta Tables**: `data/delta/{bronze,silver,gold}/`
- **Predictions**: `outputs/predictions/date=<latest>/`
- **MLflow Artifacts**: `artifacts/` and `mlruns/`
- **Airflow Logs**: `.airflow/logs/`

## 📊 Interactive Dashboard

**Streamlit Dashboard** provides comprehensive visualization:
- **Overview**: Pipeline status and key metrics
- **Predictions**: Sales forecasts with interactive charts
- **Data Analysis**: Trends, correlations, and economic indicators
- **Model Performance**: RMSE, MAE, and experiment tracking
- **Pipeline Status**: Component health and access points

**Access**: `./start_dashboard.sh` → URL displayed in terminal

## 🔧 Key Features

- **Real Data**: Uses actual Kaggle Walmart dataset
- **Economic Intelligence**: Incorporates macro-economic indicators
- **Weekly Forecasting**: Adapted for retail sales patterns
- **Production MLOps**: Full Airflow orchestration with MLflow tracking
- **Interactive Dashboard**: Streamlit visualization (MLflow UI alternative)
- **Schema Adaptation**: Automatic Walmart format mapping
- **Retry Logic**: Robust error handling and recovery

## 🎯 Production Ready

- **Scalable**: Spark-based processing for large datasets
- **Monitored**: Real-time Airflow task execution
- **Reproducible**: MLflow experiment tracking and model versioning
- **Automated**: Daily scheduling with Airflow DAGs
