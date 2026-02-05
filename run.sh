#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "🏥 Starting Simulated Patient Chatbot..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo ""
    echo "Please run setup first:"
    echo "  python3 setup.py"
    echo ""
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  WARNING: Cannot connect to Ollama at http://localhost:11434"
    echo ""
    echo "Please start Ollama first:"
    echo "  ollama serve"
    echo ""
    echo "And make sure you have pulled a model:"
    echo "  ollama pull mistral"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Run streamlit using the virtual environment
echo "Starting Streamlit..."
echo ""
./venv/bin/streamlit run app.py
