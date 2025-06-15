
# Smart Document Assistant (Trial Task – MVB)

This project is a **Minimal Viable Brain (MVB)** built for a trial task as part of an AI Engineer recruitment process.

It includes:

- **A PDF Analyzer** for processing documents.
- **A Conversational Agent** that answers questions using semantic search & LLMs.

---

## How to Run

### 1. Clone the repo

```bash
git clone https://github.com/johnvouch/lyfegen-ai-trial.git
cd document-ai-mvp
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the API

```bash
uvicorn src.api:app --reload --port 5000
```

### 4. Test it using Swagger

Go to: [http://localhost:5000/docs](http://localhost:5000/docs)

---

## API Endpoints

### `/document`
Processes a PDF and returns:
- Full text or preview (if requested)
- Detected document type
- Extracted structured fields (optional)

### `/chat`
Answers a question based on documents in the database.

---

## Notes

- Uses HuggingFace LLM and embeddings
- Vector database built with ChromaDB
- Example embeddings model: `all-MiniLM-L6-v2`
- Example LLM: `google/flan-t5-base`
