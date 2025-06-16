import os
from dotenv import load_dotenv
import tempfile
from fastapi import FastAPI, UploadFile, File, Query, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.responses import JSONResponse
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

from src.extract_text import extract_text_from_pdf
from src.extract_structured_fields import extract_structured_fields
from src.vector_db import load_vector_db

# Load .env variables.
load_dotenv()
api_key_header = APIKeyHeader(name=os.getenv("API_KEY_NAME"), auto_error=False)
api_key = os.getenv("API_KEY")

# Initialize the application.
app = FastAPI()


# Authentication.
def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == api_key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials."
        )


# Load the vector DB on startup.
db_dir = "db"
vectordb = load_vector_db(db_dir)

# Initialize the HuggingFaceHub LLM.
hf_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=512
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)


@app.post("/document")
async def process_document(
    file: UploadFile = File(...),
    full_text: bool = Query(default=False, description="Return the entire text"),
    preview_chars: int = Query(default=500, description="How many characters to preview"),
    extract_fields: bool = Query(default=False, description="Extract structured fields"),
    api_key: APIKey = Depends(get_api_key),
):
    try:
        # Save uploaded file temporarily.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            file_path = tmp.name

        # Extract raw text.
        text = extract_text_from_pdf(file_path)

        # Document classification.
        text_lower = text.lower()
        if "invoice" in text_lower:
            doc_type = "invoice"
        elif "report" in text_lower:
            doc_type = "report"
        else:
            doc_type = "contract"

        # Build response.
        response = {
            "document_type": doc_type,
            "total_characters": len(text),
        }

        # Extract structured fields.
        if extract_fields:
            fields = extract_structured_fields(text)
            response["extracted_fields"] = fields

        # Add preview or full text.
        if full_text:
            response["text"] = text
        else:
            response["text"] = text[:preview_chars]

        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/chat")
async def chat(
        question: str = Query(..., description="The question about the documents"),
        k: int = Query(default=5, description="Number of similar chunks to retrieve"),
        api_key: APIKey = Depends(get_api_key),
):
    try:
        # Set up retriever and in-memory chat buffer.
        retriever = vectordb.as_retriever(search_kwargs={"k": k})
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory
        )

        response = qa_chain.invoke({"question": question})

        # import ipdb; ipdb.set_trace()

        return JSONResponse(
            content={
                "question": question,
                "answer": response["answer"],
            }
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
