# Simulated Standardized Patient (SP) Chatbot

## Quick Start

1. Make sure Ollama is installed and running:
   ```bash
   ollama serve
   ```

2. Pull the Mistral model (if you haven't already):
   ```bash
   ollama pull mistral
   ```

3. Run the application:
   - **Windows**: Double-click `run.bat` or run from command prompt
   - **macOS/Linux**: Run `./run.sh` from terminal

4. Open your browser to `http://localhost:8501`

## Usage

1. Upload the `scenarios.xlsx` file (or your own scenario file)
2. Select a patient from the dropdown
3. Start the conversation!

## Creating Custom Scenarios

Create an Excel file with two sheets:

**Sheet 1 (Scenario Info):**
- Column A: "Scenario" - The scenario title
- Column B: "Teaching points" - Assessment rubric/goals

**Sheet 2 (Patients):**
- Column A: "Name" - Patient name
- Column B: "Characteristics" - Detailed persona and medical history

## Configuration

Set environment variables to customize:
- `OLLAMA_URL`: Ollama API URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model to use (default: mistral)

## Troubleshooting

**Can't connect to Ollama:**
- Make sure Ollama is running: `ollama serve`
- Check the URL in the error message

**Model not found:**
- Pull the model: `ollama pull mistral`
- Or set a different model: `export OLLAMA_MODEL=llama2`
