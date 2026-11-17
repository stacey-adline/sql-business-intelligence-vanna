from src.config import API_KEY, MODEL

def create_vanna_client():
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")
    try:
        from vanna.chromadb import ChromaDB_VectorStore
        from vanna.openai import OpenAI_Chat
    except ImportError as exc:
        raise RuntimeError(
            "Could not import Vanna integrations. Install dependencies with: pip install -r requirements.txt"
        ) from exc

    class BusinessVanna(ChromaDB_VectorStore, OpenAI_Chat):
        def __init__(self):
            ChromaDB_VectorStore.__init__(self, config={"path": "chroma_db"})
            OpenAI_Chat.__init__(self, config={"api_key": API_KEY, "model": MODEL})

    return BusinessVanna()
