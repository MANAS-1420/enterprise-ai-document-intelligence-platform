from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import DEFAULT_EMBEDDING_MODEL

def get_embedding_model(model_name: str = DEFAULT_EMBEDDING_MODEL):
    return HuggingFaceEmbeddings(model_name=model_name)