#!/usr/bin/env python3
"""
Setup script for Simulated Standardized Patient (SP) Chatbot
This script creates the virtual environment, installs dependencies, and generates sample data.
"""

import os
import sys
import subprocess
import venv
import platform
from pathlib import Path

def print_step(message):
    """Print a formatted step message"""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}")

def create_file(filename, content):
    """Create a file with the given content"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created {filename}")

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    try:
        subprocess.check_call(command)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        return False

def main():
    print_step("🚀 Starting Setup for SP Chatbot")
    
    # Get the current directory
    project_dir = Path.cwd()
    
    # 1. Create requirements.txt
    print_step("📝 Creating configuration files")
    
    requirements_content = """streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
requests>=2.31.0
"""
    create_file("requirements.txt", requirements_content)
    
    # 2. Create virtual environment
    print_step("🔧 Setting up virtual environment")
    
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in '{venv_dir}'...")
        venv.create(venv_dir, with_pip=True)
        print(f"✅ Virtual environment created")
    else:
        print(f"⚠️  '{venv_dir}' already exists, using existing environment")
    
    # 3. Determine paths based on OS
    is_windows = platform.system() == "Windows"
    if is_windows:
        python_executable = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_executable = os.path.join(venv_dir, "Scripts", "pip.exe")
        streamlit_executable = os.path.join(venv_dir, "Scripts", "streamlit.exe")
        activate_cmd = f"{venv_dir}\\Scripts\\activate"
    else:
        python_executable = os.path.join(venv_dir, "bin", "python")
        pip_executable = os.path.join(venv_dir, "bin", "pip")
        streamlit_executable = os.path.join(venv_dir, "bin", "streamlit")
        activate_cmd = f"source {venv_dir}/bin/activate"
    
    # 4. Install dependencies
    print_step("📦 Installing dependencies")
    
    if not run_command([python_executable, "-m", "pip", "install", "--upgrade", "pip"], 
                       "Upgrading pip"):
        sys.exit(1)
    
    if not run_command([pip_executable, "install", "-r", "requirements.txt"], 
                       "Installing required packages"):
        sys.exit(1)
    
    # 5. Generate sample Excel file
    print_step("📊 Generating sample scenario file")
    
    excel_script = """
import pandas as pd

# Data for Sheet 1: Scenario Info
data_scenario = {
    "Scenario": ["Counseling a patient about smoking cessation"],
    "Teaching points": ["Motivational interviewing; evaluate stages of change; conclude encounter with plan for treatment and follow up"]
}

# Data for Sheet 2: Patients
data_patients = {
    "Name": ["Mr. Smith", "Ms. Rodriguez"],
    "Characteristics": [
        "A 66 year old man who is hesitant about quitting smoking but is starting to have COPD symptoms and his wife is encouraging him to quit. He tried patches in the past with some success.",
        "A 45 year old woman who smokes 1 pack per day. She is pre-diabetic and minimizes the health risks of smoking. She is defensive when the topic is raised."
    ]
}

df_scenario = pd.DataFrame(data_scenario)
df_patients = pd.DataFrame(data_patients)

with pd.ExcelWriter("scenarios.xlsx", engine='openpyxl') as writer:
    df_scenario.to_excel(writer, sheet_name="Scenario Info", index=False)
    df_patients.to_excel(writer, sheet_name="Patients", index=False)

print("✅ 'scenarios.xlsx' created successfully")
"""
    
    create_file("_make_excel.py", excel_script)
    
    if run_command([python_executable, "_make_excel.py"], "Generating sample Excel file"):
        # Clean up temporary script
        os.remove("_make_excel.py")
    
    # 6. Create launch scripts
    print_step("🚀 Creating launch scripts")
    
    if is_windows:
        batch_content = f"""@echo off
echo Starting Simulated Patient Chatbot...
call {activate_cmd}
"{streamlit_executable}" run app.py
pause
"""
        create_file("run.bat", batch_content)
        print("✅ Created 'run.bat' for easy launching")
        launch_command = "run.bat"
    else:
        shell_content = f"""#!/bin/bash
echo "Starting Simulated Patient Chatbot..."
"{streamlit_executable}" run app.py
"""
        create_file("run.sh", shell_content)
        os.chmod("run.sh", 0o755)
        print("✅ Created 'run.sh' for easy launching")
        launch_command = "./run.sh"
    
    # 7. Create README
    readme_content = """# Simulated Standardized Patient (SP) Chatbot

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
"""
    create_file("README.txt", readme_content)
    
    # Final message
    print_step("✨ Setup Complete! ✨")
    print(f"""
Next steps:

1. Make sure Ollama is installed and running:
   $ ollama serve

2. Pull the Mistral model (if not already installed):
   $ ollama pull mistral

3. Start the application:
   $ {launch_command}

4. Open your browser to http://localhost:8501

Happy simulating! 🏥
""")

if __name__ == "__main__":
    main()
