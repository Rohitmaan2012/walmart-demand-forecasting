#!/bin/bash
# Airflow Startup Script for MLOps Pipeline

echo "🚀 Starting Airflow for MLOps Pipeline"
echo "====================================="

# Load configuration
if [ -f "config.env" ]; then
    echo "📋 Loading configuration from config.env..."
    export $(cat config.env | grep -v '^#' | xargs)
else
    echo "📋 Using default configuration (create config.env to customize)"
fi

# Set environment variables with defaults
export AIRFLOW_HOME="${AIRFLOW_HOME:-$(pwd)/.airflow}"
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home}"

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run 'make venv' first."
    exit 1
fi

# Kill any existing Airflow processes
echo "🧹 Cleaning up existing Airflow processes..."
pkill -f airflow 2>/dev/null || true
sleep 2

# Start Airflow webserver
echo "🌐 Starting Airflow webserver on port 8080..."
airflow webserver -p 8080 &
WEBSERVER_PID=$!

# Wait a moment for webserver to start
sleep 5

# Start Airflow scheduler
echo "⏰ Starting Airflow scheduler..."
airflow scheduler &
SCHEDULER_PID=$!

# Wait a moment for scheduler to start
sleep 5

# Check if processes are running
if ps -p $WEBSERVER_PID > /dev/null 2>&1 && ps -p $SCHEDULER_PID > /dev/null 2>&1; then
    echo "✅ Airflow started successfully!"
    echo ""
    echo "🌐 Airflow UI: http://127.0.0.1:8080"
    echo "   Username: admin"
    echo "   Password: admin"
    echo ""
    echo "📊 Your DAG: 'demand_forecast_daily'"
    echo "   - ETL → Train → Infer workflow"
    echo "   - Scheduled to run daily"
    echo "   - Can be triggered manually"
    echo ""
    echo "🛑 To stop Airflow:"
    echo "   kill $WEBSERVER_PID $SCHEDULER_PID"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Open http://127.0.0.1:8080 in your browser"
    echo "2. Login with admin/admin"
    echo "3. Find 'demand_forecast_daily' DAG"
    echo "4. Click 'Trigger DAG' to run the pipeline"
    echo "5. Watch the tasks execute: ETL → Train → Infer"
else
    echo "❌ Failed to start Airflow processes"
    echo "💡 Try running manually:"
    echo "   export AIRFLOW_HOME=\$(pwd)/.airflow"
    echo "   airflow webserver -p 8080"
    echo "   airflow scheduler"
    exit 1
fi
