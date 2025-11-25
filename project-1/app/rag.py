# app/rag.py

import os
from dotenv import load_dotenv
from shutil import rmtree
from pathlib import Path
from app.routers import convert_to_text
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# ----------------------------
# Load environment variables
# ----------------------------
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(project_root, ".env"))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# ---------------------------- 
# Paths
# ----------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))  # path to app/
vector_embeddings_dir = os.path.join(current_dir, "../embeddings")   # store embeddings here
documents_dir = Path(os.path.join(current_dir, "../Policy-Documents"))
   # your PDFs

# ----------------------------
# Ensure vector store exists or rebuild
# ----------------------------
if os.path.exists(vector_embeddings_dir):
    # Remove old embeddings to avoid dimension mismatch
    rmtree(vector_embeddings_dir)

os.makedirs(vector_embeddings_dir, exist_ok=True)

# ----------------------------
# Load documents
# ----------------------------
def load_documents_from_folder(folder: Path):
    docs = []
    for file_path in folder.iterdir():
        if file_path.suffix.lower() in [".pdf", ".docx", ".doc"]:
            text = convert_to_text.convert_to_txt(file_path)
            docs.append(Document(page_content=text, metadata={"source": str(file_path.name)}))
    return docs

docs = load_documents_from_folder(documents_dir)
# ----------------------------
# Split documents into chunks
# ----------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=100
)
chunks = splitter.split_documents(docs)

# ----------------------------
# Create embeddings
# ----------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

# ----------------------------
# Create Chroma vector store and persist
# ----------------------------
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=vector_embeddings_dir
)
vectordb.persist()

# ----------------------------
# Helper function
# ----------------------------
def get_rag_context(question: str):
    """
    Get relevant context and metadata from vector store for a question.
    """
    docs_found = vectordb.similarity_search(question, k=3)

    if not docs_found:
        return "", []

    # Concatenate document content
    context = "\n\n".join([d.page_content for d in docs_found])
    metadata_list = [d.metadata for d in docs_found]

    return context, metadata_list
