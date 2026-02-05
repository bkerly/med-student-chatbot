#Simulated Standardized Patient (SP) Chatbot
##Overview
This application is a Simulated Standardized Patient (SP) tool designed for medical education. It utilizes a local Large Language Model (LLM) to roleplay various patient personas, allowing medical students and professionals to practice history-taking, motivational interviewing, and clinical reasoning in a risk-free environment.

The application allows educators to define custom clinical scenarios and patient characteristics using external Excel files, ensuring easy modification and distribution of curriculum content.

##Prerequisites
Before installing the application, ensure the following software is installed on the host machine:

Python 3.8 or higher: Required to run the application logic.

Ollama: The local LLM backend.

Download and install Ollama from the official website.

Ensure the service is running (ollama serve).

Pull the desired model (default is mistral) by running: ollama pull mistral.

##Installation and Setup
A dedicated setup script is provided to automate the creation of the virtual environment and installation of dependencies.

Open your terminal or command prompt.

Navigate to the project directory.

Run the setup script:

Bash
python setup.py
This script will:

Create a local Python virtual environment (venv).

Install required libraries (streamlit, pandas, openpyxl, requests).

Generate the necessary execution scripts (run.bat for Windows or run.sh for macOS/Linux).

Generate a sample scenario file (scenarios.xlsx).

##Usage
1. Starting the Application
To launch the application, execute the start script generated during setup:

Windows: Double-click run.bat or run it from the command prompt.

macOS / Linux: Run ./run.sh from the terminal.

The application will open automatically in your default web browser (typically at http://localhost:8501).

##2. Loading Scenarios
The application requires a scenario definition file to function. A sample file named scenarios.xlsx is included in the root directory.

To use your own scenarios, create an Excel file (.xlsx) with the following strict structure:

Sheet 1 (Context)

Sheet Name: (Arbitrary, usually "Scenario Info")

Column A Header: Scenario (The title of the clinical module)

Column B Header: Teaching points (Rubric or goals for the learner)

Sheet 2 (Patient List)

Sheet Name: (Arbitrary, usually "Patients")

Column A Header: Name (The patient's name, e.g., "Mr. Smith")

Column B Header: Characteristics (Detailed persona instructions, medical history, and personality traits)

##3. Interacting with the Patient
Upload the .xlsx file using the sidebar uploader.

Select a patient from the dropdown menu.

Review the "Assessment Rubric" provided in the sidebar.

Type messages in the chat input field to begin the encounter.

To save the encounter, click Download Transcript in the sidebar to export a text log of the conversation.

##Configuration
The application defaults to connecting to a local Ollama instance on port 11434 using the mistral model. These settings can be modified by setting environment variables before running the application.

OLLAMA_URL: The full URL of the Ollama API (Default: http://localhost:11434)

OLLAMA_MODEL: The model tag to use for inference (Default: mistral)

##Technical Stack
Frontend: Streamlit (Python)

Data Processing: Pandas / OpenPyXL

Inference Engine: Ollama (Local LLM)

Communication: REST API (via Python Requests)