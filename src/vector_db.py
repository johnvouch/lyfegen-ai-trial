from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def load_vector_db(persist_dir: str = "db"):
    """
    Loads the Chroma vector database using the HuggingFace embedding model.

    Parameters
    ----------
    persist_dir : str
        Path to the directory where Chroma DB is saved.

    Returns
    -------
    Chroma
        A loaded vector store ready for similarity search.

    """

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)

    return vectordb
