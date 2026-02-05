# Simulated Standardized Patient (SP) Chatbot

A medical education tool that uses local LLMs to simulate patient encounters for training healthcare professionals.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)

2. **Ollama** - Install the local LLM server:
   - Download from [ollama.ai](https://ollama.ai)
   - Install and start the service:
     ```bash
     ollama serve
     ```
   - Pull the Mistral model:
     ```bash
     ollama pull mistral
     ```

### Installation

1. **Run the setup script:**
   ```bash
   python3 setup.py
   ```
   
   This will:
   - Create a Python virtual environment
   - Install all dependencies
   - Generate a sample scenario file
   - Create launch scripts

2. **Start the application:**
   - **macOS/Linux:** `./run.sh`
   - **Windows:** Double-click `run.bat`

3. **Open your browser** to `http://localhost:8501`

## 📖 How to Use

1. **Upload a scenario file** - Use the sidebar to upload `scenarios.xlsx` or your own file
2. **Select a patient** - Choose from the dropdown menu
3. **Review the rubric** - Check the assessment criteria in the sidebar
4. **Start the conversation** - Type messages to practice your clinical skills
5. **Download transcript** - Save the conversation for review or grading

## 🎯 Features

- ✅ Multiple patient personas per scenario
- ✅ Customizable via Excel files (no coding required)
- ✅ Realistic patient responses using local LLMs
- ✅ Session transcripts for review
- ✅ Assessment rubrics for self-evaluation
- ✅ Privacy-focused (runs entirely on your machine)

## 📊 Creating Custom Scenarios

Create an Excel file (`.xlsx`) with this structure:

### Sheet 1: "Scenario Info"
| Scenario | Teaching points |
|----------|----------------|
| Scenario title | Assessment rubric or learning objectives |

### Sheet 2: "Patients"
| Name | Characteristics |
|------|----------------|
| Patient name | Detailed persona, medical history, personality traits |

**Example:**

**Sheet 1:**
| Scenario | Teaching points |
|----------|----------------|
| Smoking cessation counseling | Motivational interviewing; assess readiness to change; create action plan |

**Sheet 2:**
| Name | Characteristics |
|------|----------------|
| Mr. Smith | 66yo male, hesitant about quitting, early COPD, tried patches before |
| Ms. Rodriguez | 45yo female, 1 PPD, pre-diabetic, defensive about smoking |

## ⚙️ Configuration

Customize the chatbot using environment variables:

```bash
# Change Ollama URL (default: http://localhost:11434)
export OLLAMA_URL="http://your-server:11434"

# Use a different model (default: mistral)
export OLLAMA_MODEL="llama2"
```

Available models (must be pulled first):
- `mistral` - Fast, balanced performance (recommended)
- `llama2` - Good alternative
- `mixtral` - Larger, more capable (requires more RAM)

To pull a model:
```bash
ollama pull mistral
```

## 🔧 Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check if the service is accessible: `curl http://localhost:11434/api/tags`
- Verify firewall settings aren't blocking port 11434

### "Model not found"
- Pull the model: `ollama pull mistral`
- Check available models: `ollama list`
- Update the MODEL variable if using a different model

### "Excel file error"
- Ensure your Excel file has exactly 2 sheets
- Verify column names match exactly: "Scenario", "Teaching points", "Name", "Characteristics"
- Check for hidden characters or extra spaces in headers

### Performance issues
- Try a smaller model: `ollama pull mistral:7b`
- Close other applications to free up RAM
- Reduce conversation length (use Reset button)

## 🛠️ Technical Details

**Stack:**
- Frontend: Streamlit
- LLM Backend: Ollama (local)
- Data: Pandas + OpenPyXL
- Language: Python 3.8+

**Privacy:**
- All data stays on your machine
- No internet connection required after setup
- No data sent to external servers

## 📚 Educational Use Cases

- **Medical Students:** Practice history-taking and communication skills
- **Residents:** Rehearse difficult conversations (breaking bad news, end-of-life discussions)
- **Faculty:** Create standardized scenarios for assessment
- **Continuing Education:** Practice motivational interviewing, shared decision-making

## 🤝 Tips for Effective Use

1. **Start broad:** Use open-ended questions
2. **Build rapport:** Don't rush into medical questions
3. **Listen actively:** The AI patient will respond to your approach
4. **Review transcripts:** Identify areas for improvement
5. **Compare approaches:** Try the same scenario with different communication styles

## 📝 License

This project is provided as-is for educational purposes.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Ollama](https://ollama.ai)
- Uses [Pandas](https://pandas.pydata.org/) for data handling

---

**Need help?** Check the troubleshooting section or review the sample `scenarios.xlsx` file for formatting examples.
