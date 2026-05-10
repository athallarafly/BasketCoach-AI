# 🏀 BasketCoach-AI

**BasketCoach-AI** is a smart basketball coaching assistant powered by **Google Gemini LLM** and **RAG (Retrieval-Augmented Generation)** architecture. This system allows users to interactively ask about basketball rules, techniques, strategies, and history through a sleek Streamlit interface.

### 📺 App Demo
<img width="2547" height="1334" alt="BasketCoach-AI Interface" src="https://github.com/user-attachments/assets/29bab19c-0392-4475-a90c-9987ac6fbc6e" />

## 🚀 Key Features
- **RAG-Powered:** Delivers accurate answers based on official basketball documents (PDF) processed via FAISS.
- **Streaming Responses:** Smooth, ChatGPT-like typing effect for a responsive user experience.
- **Smart Welcome Cards:** Quick-access buttons for popular topics to guide new users.
- **Session History & Search:** Save chat sessions and easily filter through past conversations.
- **Visual Aids:** Automatically displays technical diagrams (e.g., court dimensions) when relevant.

## 🏗️ Project Flow (Architecture)

The project operates in two main phases: **Data Ingestion** and the **Chatbot Interface**.



1.  **Ingestion Phase (`script_ingest.ipynb`):**
    - Reads PDF documents from the `data/` folder.
    - Breaks down the text into manageable pieces (*chunking*).
    - Converts text into vectors (embeddings) using `models/gemini-embedding-2`.
    - Stores these vectors in a local **FAISS** database.

2.  **Retrieval & Generation Phase (`app.py`):**
    - User provides input through the Streamlit UI.
    - The system retrieves the most relevant text chunks from the FAISS database.
    - These chunks are sent to the Gemini LLM as context along with the user's query.
    - Gemini generates an accurate, helpful response in a professional coaching tone.

## 🛠️ Setup & Installation

### 1. Requirements
- Python 3.9+
- Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/))

### 2. Installation
Clone this repository and navigate to the project directory:
```bash
git clone [https://github.com/username/BasketCoach-AI.git](https://github.com/username/BasketCoach-AI.git)
cd BasketCoach-AI
```
### 3. Environment Configuration
Create a .env file in the root directory and add your API key:

Code snippet
GEMINI_API_KEY=your_api_key_here

📖 How to Run
Follow these steps to get the assistant up and running:

Step 1: Ingest Data
Open and run all cells in script_ingest.ipynb. This will process your PDFs in the data/ folder and generate the faiss_index_basket folder.

Step 2: Launch the App
Once the FAISS index is created, run the Streamlit application:

Bash
python -m streamlit run app.py
The app will be available in your browser, typically at http://localhost:8501
