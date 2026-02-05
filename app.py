import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- Configuration ---
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# --- Helper Functions ---

def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def load_scenarios_from_excel(uploaded_file):
    """Load scenario and patient data from Excel file"""
    try:
        xls = pd.ExcelFile(uploaded_file)
        
        # Parse Sheet 1: Context/Rubric
        df_context = pd.read_excel(xls, sheet_name=0)
        scenario_title = df_context.get("Scenario", ["Unknown Scenario"])[0]
        teaching_points = df_context.get("Teaching points", ["No rubric provided."])[0]
        
        # Parse Sheet 2: Patients
        df_patients = pd.read_excel(xls, sheet_name=1)
        
        if "Name" not in df_patients.columns or "Characteristics" not in df_patients.columns:
            st.error("Sheet 2 must contain 'Name' and 'Characteristics' columns.")
            return None

        patients = {}
        for _, row in df_patients.iterrows():
            name = str(row['Name'])
            characteristics = str(row['Characteristics'])
            
            # Create a shorter preview for the dropdown
            char_preview = (characteristics[:50] + '...') if len(characteristics) > 50 else characteristics
            label = f"{name} - {char_preview}"
            
            patients[label] = {
                "name": name,
                "persona": characteristics,
                "scenario_title": scenario_title,
                "rubric": teaching_points
            }
            
        return patients
        
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return None

def query_ollama(messages):
    """Send messages to Ollama and get response"""
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    try:
        response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result.get("message", {}).get("content", "No response from model.")
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The model may be taking too long to respond."
    except requests.exceptions.RequestException as e:
        return f"Error contacting Ollama: {e}"

# --- Main App ---

st.set_page_config(page_title="Simulated Patient Chatbot", layout="wide")
st.title("🏥 Simulated Standardized Patient (SP) Chatbot")

# Check Ollama connection
if not check_ollama_connection():
    st.error(f"⚠️ Cannot connect to Ollama at {OLLAMA_URL}. Please ensure Ollama is running.")
    st.info("To start Ollama, run: `ollama serve` in your terminal")
    st.stop()

with st.sidebar:
    st.header("📋 Scenario Setup")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload Scenario Excel (.xlsx)", type=["xlsx"])
    
    patients_data = {}
    current_patient = None
    
    if uploaded_file:
        patients_data = load_scenarios_from_excel(uploaded_file)
        
    if patients_data:
        selected_label = st.selectbox("Choose Patient", options=list(patients_data.keys()))
        current_patient = patients_data[selected_label]
        
        st.markdown("---")
        st.subheader("📖 Scenario")
        st.write(current_patient['scenario_title'])
        
        st.subheader("👤 Patient Persona")
        st.info(current_patient['persona'])
        
        st.subheader("✅ Assessment Rubric")
        st.success(current_patient['rubric'])
    else:
        st.warning("Please upload a scenario file to begin.")

    st.markdown("---")
    
    # Reset conversation
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Download transcript
    if st.session_state.get('messages'):
        transcript = ""
        for msg in st.session_state.messages:
            role = "DOCTOR" if msg["role"] == "user" else "PATIENT"
            transcript += f"{role}: {msg['content']}\n\n"
        
        st.download_button(
            "💾 Download Transcript",
            transcript,
            f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            use_container_width=True
        )

# --- Chat Interface ---

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role_label = "Doctor (You)" if message["role"] == "user" else "Patient"
    avatar = "👨‍⚕️" if message["role"] == "user" else "🤒"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(f"**{role_label}:** {message['content']}")

# Chat input
if current_patient:
    if prompt := st.chat_input("Type your message to the patient..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👨‍⚕️"):
            st.markdown(f"**Doctor (You):** {prompt}")

        # Create system prompt
        system_prompt = (
            f"You are roleplaying as {current_patient['name']}, a patient in a medical encounter.\n\n"
            f"Persona details: {current_patient['persona']}\n\n"
            "IMPORTANT INSTRUCTIONS:\n"
            "- You are the PATIENT, not the doctor\n"
            "- Respond AS the patient would respond\n"
            "- Keep responses natural and conversational (2-4 sentences)\n"
            "- Stay consistent with your medical history and personality\n"
            "- Show realistic emotions and concerns\n"
            "- Don't volunteer information unless asked\n"
            "- Be realistic - patients may be nervous, evasive, or uncertain"
        )

        # Prepare messages for API
        api_messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in st.session_state.messages:
            api_messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Get response from Ollama
        with st.chat_message("assistant", avatar="🤒"):
            with st.spinner("Patient is thinking..."):
                response_text = query_ollama(api_messages)
                st.markdown(f"**Patient:** {response_text}")
        
        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()
else:
    st.info("👈 Upload a scenario Excel file in the sidebar to start the simulation")
    
    with st.expander("ℹ️ How to use this application"):
        st.markdown("""
        1. **Upload a scenario file** using the sidebar uploader
        2. **Select a patient** from the dropdown menu
        3. **Review the scenario** and assessment rubric in the sidebar
        4. **Start the conversation** by typing in the chat input
        5. **Download the transcript** when finished for review
        
        **Tips:**
        - Practice open-ended questions
        - Build rapport before diving into sensitive topics
        - Use motivational interviewing techniques
        - Pay attention to the assessment rubric
        """)
