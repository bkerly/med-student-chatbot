# TROUBLESHOOTING: "No module named streamlit"

## The Problem
You're getting this error because you're running Python globally instead of using the virtual environment where Streamlit is installed.

## The Solution

### Option 1: Use the run.sh script (RECOMMENDED)
```bash
cd ~/Documents/med-student-chatbot
./run.sh
```

### Option 2: Run Streamlit directly from the virtual environment
```bash
cd ~/Documents/med-student-chatbot
./venv/bin/streamlit run app.py
```

### Option 3: Activate the virtual environment first
```bash
cd ~/Documents/med-student-chatbot
source venv/bin/activate
streamlit run app.py
```

## If You Haven't Run Setup Yet

If you see "Virtual environment not found", run setup first:

```bash
cd ~/Documents/med-student-chatbot
python3 setup.py
```

This will:
- Create a virtual environment in `venv/`
- Install all dependencies (streamlit, pandas, etc.)
- Generate the sample scenarios.xlsx file
- Create the run.sh script

## Why This Happens

When you run `/usr/local/bin/python3`, you're using the system Python, which doesn't have Streamlit installed. The setup script installs Streamlit into a virtual environment (`venv/`), which keeps your project dependencies separate from your system Python.

## Step-by-Step Fix

1. **Navigate to your project:**
   ```bash
   cd ~/Documents/med-student-chatbot
   ```

2. **Run setup (if you haven't already):**
   ```bash
   python3 setup.py
   ```

3. **Start Ollama (in a separate terminal):**
   ```bash
   ollama serve
   ```

4. **Pull the Mistral model (first time only):**
   ```bash
   ollama pull mistral
   ```

5. **Run the app:**
   ```bash
   ./run.sh
   ```

6. **Open your browser to:** http://localhost:8501

## Common Issues

### "permission denied: ./run.sh"
Make it executable:
```bash
chmod +x run.sh
```

### "curl: command not found" in run.sh
The script will still work - it just can't check if Ollama is running. Make sure you start Ollama manually first.

### "command not found: ollama"
Install Ollama:
- Download from https://ollama.ai
- Or use Homebrew: `brew install ollama`

## Quick Reference

**Setup (once):**
```bash
cd ~/Documents/med-student-chatbot
python3 setup.py
ollama pull mistral
```

**Run (every time):**
```bash
# Terminal 1 (if Ollama isn't running as a service)
ollama serve

# Terminal 2
cd ~/Documents/med-student-chatbot
./run.sh
```
