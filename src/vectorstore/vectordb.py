from typing import List
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma

def build_faiss_vectorstore(chunks: List, embedding_model):
    return FAISS.from_documents(chunks, embedding_model)

def build_chroma_vectorstore(chunks: List, embedding_model, persist_directory: str = "data/vectorstore/chroma"):
    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )