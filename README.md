# Smart Document Assistant (Trial Task – MVB)

This project is a **Minimal Viable Brain (MVB)** built for a trial task as part of an AI Engineer recruitment process.

It includes:
- A **PDF Analyzer** for processing documents.
- A **Conversational Agent** that answers questions using semantic search & LLMs.

---

## Tech Stack

- **FastAPI** – Backend web framework  
- **LangChain** – LLM orchestration & vector retrieval  
- **HuggingFaceHub** – Open-source LLM integration  
- **Chroma DB** – Vector database  
- **PyMuPDF** – PDF text extraction  
- **Python 3.9+**

---

## Project Structure

project/
│
├── src/
│ ├── api.py # Main FastAPI app with two endpoints
│ ├── extract_text.py # PDF text extraction & chunking
│ ├── extract_structured_fields.py # Structured data extraction logic
│ └── vector_db.py # Chroma vector DB setup & loading
│
├── db/ # Chroma database
├── requirements.txt
└── README.md

---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/johnvouch/lyfegen-ai-trial.git
cd document-ai-mvp


### 2. Install dependencies
pip install -r requirements.txt


### 3. Launch the API
uvicorn src.api:app --reload --port 5000


### 4. Test it using Swagger at
http://localhost:5000/docs

---

API Endpoints

/document
Processes a PDF and returns:

- Document type (contract, invoice, report)
- Extracted structured fields (e.g. parties, country, disease)
- Full or preview text (configurable)

/chat
- You ask a question, it searches the existing vector DB, and responds using a HuggingFace LLM.
- No PDF upload required (uses existing DB)
- Accepts a question and returns an LLM-generated answer
