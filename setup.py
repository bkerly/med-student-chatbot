import os
import sys
import subprocess
import venv
import platform

# --- 1. Define File Contents ---

REQUIREMENTS_TXT = """streamlit
pandas
openpyxl
requests
"""

APP_PY_CONTENT = """import streamlit as st
import pandas as pd
import requests
import json
import os
import time
from datetime import datetime

# --- Configuration ---
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "mistral") 

# --- Helper Functions ---

def load_scenarios_from_excel(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        
        # Parse Sheet 1: Context/Rubric (First sheet)
        df_context = pd.read_excel(xls, sheet_name=0)
        # Handle case where header might be slightly different; allow flexible lookup if needed
        # For now, we assume strict column names per instructions
        scenario_title = df_context.get("Scenario", ["Unknown Scenario"])[0]
        teaching_points = df_context.get("Teaching points", ["No rubric provided."])[0]
        
        # Parse Sheet 2: Patients (Second sheet)
        df_patients = pd.read_excel(xls, sheet_name=1)
        
        if "Name" not in df_patients.columns or "Characteristics" not in df_patients.columns:
            st.error("Sheet 2 must contain 'Name' and 'Characteristics' columns.")
            return None

        patients = {}
        for _, row in df_patients.iterrows():
            char_preview = (row['Characteristics'][:50] + '..') if len(str(row['Characteristics'])) > 50 else str(row['Characteristics'])
            label = f"{row['Name']} - {char_preview}"
            
            patients[label] = {
                "name": row['Name'],
                "persona": row['Characteristics'],
                "scenario_title": scenario_title,
                "rubric": teaching_points
            }
            
        return patients
        
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return None

def query_ollama(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    try:
        response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("message", {}).get("content", "No response from model.")
    except requests.exceptions.RequestException as e:
        return f"Error contacting Ollama: {e}"

# --- Main App ---

st.set_page_config(page_title="Simulated Patient Chatbot", layout="wide")
st.title("Simulated Standardized Patient (SP) Chatbot")

with st.sidebar:
    st.header("1. Scenario Setup")
    uploaded_file = st.file_uploader("Upload Scenario Excel (.xlsx)", type=["xlsx"])
    
    patients_data = {}
    current_patient = None
    
    if uploaded_file:
        patients_data = load_scenarios_from_excel(uploaded_file)
        
    if patients_data:
        selected_label = st.selectbox("Choose Patient", options=list(patients_data.keys()))
        current_patient = patients_data[selected_label]
        
        st.markdown("---")
        st.subheader("Scenario: " + str(current_patient['scenario_title']))
        st.subheader("Patient Persona")
        st.info(current_patient['persona'])
        st.subheader("Assessment Rubric")
        st.success(current_patient['rubric'])
    else:
        st.warning("Please upload a scenario file to begin.")

    st.markdown("---")
    if st.button("Reset / Clear Conversation"):
        st.session_state.messages = []

    if st.session_state.get('messages'):
        transcript = ""
        for msg in st.session_state.messages:
            role = "DOCTOR" if msg["role"] == "user" else "PATIENT"
            transcript += f"{role}: {msg['content']}\\n\\n"
        st.download_button("Download Transcript", transcript, f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# --- Chat Interface ---

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role_label = "Doctor (You)" if message["role"] == "user" else "Patient"
    avatar = "👨‍⚕️" if message["role"] == "user" else "🤒"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(f"**{role_label}:** {message['content']}")

if current_patient:
    if prompt := st.chat_input("Type your message to the patient..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👨‍⚕️"):
            st.write(f"**Doctor (You):** {prompt}")

        system_prompt = (
            f"You are roleplaying as {current_patient['name']}, a patient in a medical encounter. "
            f"Persona details: {current_patient['persona']}\\n\\n"
            "IMPORTANT: You are the PATIENT, not the doctor. Respond AS the patient. "
            "Keep responses natural, concise (2-4 sentences), and consistent with your history."
        )

        api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        
        with st.chat_message("assistant", avatar="🤒"):
            with st.spinner("Patient is thinking..."):
                response_text = query_ollama(api_messages)
                st.write(f"**Patient:** {response_text}")
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})
else:
    st.info("👈 Upload a scenario Excel file in the sidebar to start.")
"""

# Script to generate Excel (requires pandas, so we run this AFTER venv install)
EXCEL_GENERATOR_SCRIPT = """
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

with pd.ExcelWriter("scenarios.xlsx") as writer:
    df_scenario.to_excel(writer, sheet_name="Scenario Info", index=False)
    df_patients.to_excel(writer, sheet_name="Patients", index=False)

print("✅ 'scenarios.xlsx' created successfully.")
"""

# --- 2. Setup Logic ---

def create_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 Created {filename}")

def main():
    print("🚀 Starting Setup for SP Chatbot...")

    # 1. Create source files
    create_file("requirements.txt", REQUIREMENTS_TXT)
    create_file("app.py", APP_PY_CONTENT)
    create_file("_make_excel.py", EXCEL_GENERATOR_SCRIPT)

    # 2. Create Virtual Environment
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print(f"📦 Creating virtual environment in '{venv_dir}'...")
        venv.create(venv_dir, with_pip=True)
    else:
        print(f"📦 '{venv_dir}' already exists.")

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

    # 4. Install Dependencies
    print("⬇️  Installing dependencies...")
    try:
        subprocess.check_call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

    # 5. Generate Excel File (using the environment we just built)
    print("📊 Generating sample Excel file...")
    try:
        subprocess.check_call([python_executable, "_make_excel.py"])
        os.remove("_make_excel.py") # Clean up
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating Excel file: {e}")

    # 6. Create Launch Scripts
    if is_windows:
        with open("run.bat", "w") as f:
            f.write(f'@echo off\ncall "{activate_cmd}"\n"{streamlit_executable}" run app.py\npause')
        print("✅ Created 'run.bat' for easy launching.")
    else:
        with open("run.sh", "w") as f:
            f.write(f'#!/bin/bash\n"{streamlit_executable}" run app.py')
        os.chmod("run.sh", 0o755)
        print("✅ Created 'run.sh' for easy launching.")

    print("\n✨ Setup Complete! ✨")
    print(f"To start the app, run: {'run.bat' if is_windows else './run.sh'}")

if __name__ == "__main__":
    main()