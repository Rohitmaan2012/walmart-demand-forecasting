#!/bin/bash

echo "🚀 Starting Walmart MLOps Dashboard"
echo "=================================="

# Load configuration
if [ -f "config.env" ]; then
    echo "📋 Loading configuration from config.env..."
    export $(cat config.env | grep -v '^#' | xargs)
else
    echo "📋 Using default configuration (create config.env to customize)"
fi

echo "📦 Activating virtual environment..."
if [ -d ".venv" ]; then
    . .venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run 'make venv' first."
    exit 1
fi

# Get configuration values
STREAMLIT_PORT=${STREAMLIT_PORT:-8501}
STREAMLIT_HOST=${STREAMLIT_HOST:-127.0.0.1}

echo "🌐 Starting Streamlit dashboard on port $STREAMLIT_PORT..."
echo "   Dashboard URL: http://$STREAMLIT_HOST:$STREAMLIT_PORT"
echo ""
echo "📊 Dashboard Features:"
echo "   • Overview of pipeline status"
echo "   • Sales predictions visualization"
echo "   • Data analysis and trends"
echo "   • Model performance metrics"
echo "   • Pipeline component status"
echo ""
echo "🛑 To stop dashboard: Ctrl+C"
echo ""

streamlit run dashboard.py --server.port $STREAMLIT_PORT --server.address $STREAMLIT_HOST
